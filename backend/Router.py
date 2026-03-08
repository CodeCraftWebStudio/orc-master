###################################################################################################################
#   ROUTER.PY
#   THE CENTER OF BACKEND OPERATIONS
#   NOTE THAT THE USER ROTATION SHOULD ALWAYS COME AFTER ERROR CHECKS, NEVER BEFORE, TO PREVENT BROKEN REQUESTS
#   AND SESSION KEYS
###################################################################################################################

from flask import Flask
from flask_cors import CORS
from .models.model_base.events_model import CalendarEvent
from backend.models.model_base.user_services.services import (
    check_if_a_user_has_logged_in_with_a_role,
    get_user_by_key,
    register_user,
    create_anonymous_user,
    check_user_registered_from_user,
    check_user_registered_from_session_key,
    User,
    get_total_user_count,
    RoleType,
    db,
    get_all_contacts
)
from backend.models.model_base.user_services.executive_base import EXECUTIVE_ROLES
import os
from flask import Flask, jsonify, redirect, request, Response, stream_with_context
from functools import wraps
from .error_messages.errors import (
    ValidationError,
    AuthenticationError,
    AuthorizationError,
    NotFoundError,
    ensure_requirements,
    session_key_required
)
from .Database import app
from .local_storage import localStorage
from cryptography.fernet import Fernet
from backend.models.security import generate_secret_key, reversible_dehasher, reversible_hasher
from backend.learn.config import generate_quiz
from datetime import datetime
from backend.models.model_base.general_base import create_db
from backend.chatroom.Models.room import Room
from backend.chatroom.Models.message import Message
from backend.chatroom.Services.professional import SYSTEM_INSTRUCTIONS
from flask_socketio import SocketIO, emit, join_room, leave_room
from backend.models.secret_key_generator import api
import google.generativeai as genai


CORS(
    app,
    supports_credentials=True,
    resources={
        r"/*": {"origins": "https://boisterous-alfajores-6bcd79.netlify.app"}}
)

# -------------------------------
# Configuration
# -------------------------------
LOCAL_STORAGE = localStorage
GET, POST, UPDATE, DELETE = "GET", "POST", "UPDATE", "DELETE"
SECRET_KEY = LOCAL_STORAGE.getItem('ORC')
socketio = SocketIO(app, cors_allowed_origins="*", manage_session=False)

try:
    print(Fernet(SECRET_KEY))
except Exception as e:
    print(f"Invalid secret key {SECRET_KEY}. Error: {e}")
    SECRET_KEY = b"Xh84PtDmGYycPnlLCyPLBVYBzpUZbPJdA2t2zxJhZKQ="
    print(f"Forced secret key to: {SECRET_KEY}")


def hash_text(text):
    return reversible_hasher(text, SECRET_KEY)


def dehash_text(text):
    return reversible_dehasher(text, SECRET_KEY)

# -------------------------------
# User Endpoints
# -------------------------------


@app.route('/api/user/start', methods=[GET, POST])
def start_user_session():
    user = create_anonymous_user()
    if not user or not user.session_key:
        return jsonify({"error": "User/session key invalid"}), 404
    return jsonify({"session_key": reversible_hasher(user.session_key, SECRET_KEY)})


@app.route('/api/user/getTotalMembers', methods=[GET])
def get_total_members():
    return jsonify(get_total_user_count())


@app.route('/api/user/getIsUserRegistered', methods=["POST"])
def get_user_registered():
    data = request.get_json()
    session_key = data.get("session_key")
    if not session_key:
        return jsonify({"error": "Session key not given"}), 400
    user = get_user_by_key(session_key)
    if user and user.name not in ["Anonymous", "Unassigned"] and user.role_type != RoleType.GUEST:
        return jsonify({"result": "t"})
    return jsonify({"result": "f"})


@ensure_requirements(requirements=["session_key", "name", "school_class"])
@app.route('/api/user/registerUser', methods=[POST])
def register_user_as_a_member():
    data = request.get_json()
    user = get_user_by_key(reversible_dehasher(
        data.get("session_key"), SECRET_KEY))
    register_user(user, data.get("name"), data.get("school_class"))
    return jsonify(reversible_hasher(user.session_key, SECRET_KEY))


@ensure_requirements(requirements=["session_key", "name", "school_class", "role_name", "role_code"])
@app.route('/api/user/registerUser/Executive', methods=['POST'])
def register_user_as_executive():
    data = request.get_json()
    user = get_user_by_key(data["session_key"])
    if not user:
        return jsonify({"error": "Invalid session"}), 401

    role_name, role_code = data["role_name"], data["role_code"]
    if role_name not in EXECUTIVE_ROLES:
        return jsonify({"error": "Invalid role"}), 400
    role_meta = EXECUTIVE_ROLES[role_name]
    if role_meta["code"] != role_code:
        return jsonify({"error": "Invalid code for role"}), 403
    if check_if_a_user_has_logged_in_with_a_role(role_name):
        return jsonify({"error": "Role already taken"}), 409

    register_user(user, data["name"], data["school_class"])
    user.role_title = role_name
    user.role_type = role_meta["role_type"]
    user.rotate_key()
    db.session.commit()

    return jsonify({
        "session_key": hash_text(user.session_key),
        "role": role_name,
        "role_type": user.role_type
    })


@app.route('/api/ai/generateQuizQuestions', methods=[POST])
def generateQuizQuestions():
    data = request.get_json(force=True)
    if not data or not data.get("pageText") or not data.get("difficulty") or not data.get("session_key"):
        return jsonify({"error": "Missing required fields"}), 400
    if len(data["pageText"]) > 20_000:
        return jsonify({"error": "Text too long"}), 413
    user = get_user_by_key(reversible_dehasher(
        data["session_key"], SECRET_KEY))
    if not user:
        return jsonify({"error": "Invalid session key"}), 401
    user.rotate_key()
    quiz_json = generate_quiz(data["difficulty"], data["pageText"]).parsed
    return jsonify({"result": quiz_json, "session_key": reversible_hasher(user.session_key, SECRET_KEY)})


@app.route('/api/user/getUserDetails', methods=["POST"])
def get_user_details():
    data = request.get_json()
    session_key = data.get("session_key")
    if not session_key:
        return jsonify({"error": "No session key provided"}), 400
    user = get_user_by_key(session_key)
    if not user:
        return jsonify({"error": "Invalid session key"}), 401
    return jsonify({
        'name': user.name,
        'school_class': user.school_class,
        'role_type': user.role_type,
        'role_title': user.role_title
    })


@app.route('/api/tools/getHashedValue', methods=['POST'])
def get_hashed_value():
    data = request.get_json()
    if not data.get("value"):
        return jsonify({"error": "Invalid input"}), 400
    return jsonify({"result": hash_text(data.get("value"))})


@app.route('/api/tools/getDehashedValue', methods=['POST'])
def get_dehashed_value():
    data = request.get_json()
    if not data.get("value"):
        return jsonify({"error": "Invalid input"}), 400
    return jsonify({"result": dehash_text(data.get("value"))})


@app.route('/api/roles/status', methods=['GET'])
def get_roles_status():
    roles = []
    for name, meta in EXECUTIVE_ROLES.items():
        roles.append({
            "name": name,
            "label": meta["label"],
            "taken": check_if_a_user_has_logged_in_with_a_role(name)
        })
    return jsonify(roles)

# -------------------------------
# Database / Events
# -------------------------------


@app.route('/api/database/events', methods=['POST'])
@session_key_required
def event_operations():
    data = request.get_json()
    op = data.get("op", "read")
    user = get_user_by_key(data["session_key"])
    if not user:
        return AuthenticationError("Invalid session").to_response()

    if op == "read":
        events = CalendarEvent.query.order_by(CalendarEvent.date).all()
        return jsonify([e.to_dict() for e in events])

    if user.role_type != RoleType.ADMIN:
        return AuthorizationError("Admin required").to_response()

    if op == "create":
        event = CalendarEvent.create(
            date_obj=datetime.fromisoformat(data["date_obj"]).date(),
            time_obj=data.get("time_obj"),
            description_obj=data["description_obj"]
        )
        return jsonify(event.to_dict())

    if op == "update":
        event = CalendarEvent.query.get(data["id"])
        if not event:
            return ValidationError("Event not found").to_response()
        event.update(data.get("new_time"), data.get("new_description"))
        return jsonify(event.to_dict())

    if op == "delete":
        event = CalendarEvent.query.get(data["id"])
        if not event:
            return ValidationError("Event not found").to_response()
        event.delete()
        return jsonify({"status": "deleted"})

    return ValidationError("Invalid operation").to_response()

# -------------------------------
# Chat / SocketIO
# -------------------------------


def ensure_global_room():
    if not Room.query.filter_by(name="global").first():
        db.session.add(Room(name="global"))
    if not Room.query.filter_by(name="executives").first():
        db.session.add(Room(name="executives"))
    db.session.commit()


@app.route("/api/chat/getUsers")
def get_users():
    return jsonify(get_all_contacts())


@app.route("/api/chat/getRoom/<room_name>")
def get_room(room_name):
    room = Room.query.filter_by(name=room_name).first()
    if not room:
        return jsonify({"error": "Room not found"}), 404
    return jsonify({"room_id": room.id})


@app.route("/api/chat/getMessages/<int:room_id>")
def get_messages(room_id):
    messages = Message.query.filter_by(
        room_id=room_id).order_by(Message.timestamp).all()
    for m in messages:
        if m.status == "sent":
            m.status = "delivered"
    db.session.commit()
    return jsonify([{
        "id": m.id,
        "content": m.content,
        "user_id": m.user_id,
        "username": m.user.name,
        "timestamp": m.timestamp.isoformat(),
        "status": m.status
    } for m in messages])


@app.route("/api/chat/send", methods=["POST"])
def send_message_api():
    data = request.get_json()
    message = Message(
        content=data["content"], user_id=data["user_id"], room_id=data["room_id"], status="sent")
    db.session.add(message)
    db.session.commit()
    return jsonify({"status": "ok"})


@socketio.on("connect")
def handle_connect():
    print("Client connected")


@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")


@socketio.on("join")
def handle_join(data):
    session_key = data.get("session_key")
    room_name = data.get("room") or "global"
    user = get_user_by_key(dehash_text(session_key))
    if not user:
        return emit("error", {"error": "User not found"})
    if room_name == "executives" and user.role_type in [RoleType.GUEST, RoleType.MEMBER]:
        return emit("error", {"error": "Not authorized"})
    room = Room.query.filter_by(name=room_name).first()
    if not room:
        return emit("error", {"error": "Room not found"})
    join_room(room_name)
    emit("user_online", {"user_id": user.id,
         "username": user.name}, broadcast=True)


@socketio.on("send_message")
def handle_send_message(data):
    session_key = data.get("session_key")
    content = data.get("content")
    room_name = data.get("room") or "global"
    user = get_user_by_key(dehash_text(session_key))
    if not user:
        return emit("error", {"error": "User not found"})
    room = Room.query.filter_by(name=room_name).first()
    if not room:
        return emit("error", {"error": "Room not found"})
    message = Message(content=content, user_id=user.id,
                      room_id=room.id, status="delivered")
    db.session.add(message)
    db.session.commit()
    emit("receive_message", {
        "id": message.id,
        "content": message.content,
        "user_id": user.id,
        "username": user.name,
        "timestamp": message.timestamp.isoformat(),
        "status": message.status,
        "room": room_name
    }, room=room_name)


@socketio.on("typing")
def handle_typing(data):
    session_key = data.get("session_key")
    room_name = data.get("room") or "global"
    state = data.get("typing", False)
    user = get_user_by_key(dehash_text(session_key))
    if not user:
        return emit("error", {"error": "User not found"})
    emit("user_typing", {"user_id": user.id, "username": user.name,
         "typing": state}, room=room_name, include_self=False)


@socketio.on("leave")
def handle_leave(data):
    room_name = data.get("room") or "global"
    leave_room(room_name)


@app.route("/api/chat/getPrivateRoom/<int:other_user_id>", methods=["POST"])
def get_private_room(other_user_id):
    data = request.get_json()
    session_key = data.get("session_key")
    user = get_user_by_key(dehash_text(session_key))
    if not user:
        return jsonify({"error": "Invalid session"}), 401
    if user.id == other_user_id:
        return jsonify({"error": "Cannot create private room with yourself"}), 400
    smaller, larger = min(user.id, other_user_id), max(user.id, other_user_id)
    room_name = f"private_{smaller}_{larger}"
    room = Room.query.filter_by(name=room_name).first()
    if not room:
        room = Room(name=room_name)
        db.session.add(room)
        db.session.commit()
    return jsonify({"room_name": room_name, "room_id": room.id})


# -------------------------------
# Google Generative AI / Gemini
# -------------------------------
genai.configure(api_key=api)
model = genai.GenerativeModel("gemini-2.5-flash-lite")


def build_prompt(message: str, history: list) -> str:
    return f"""
{SYSTEM_INSTRUCTIONS}

History:
{history}

Current Request:
{message}
"""


def gemini_stream(prompt: str, max_chunks: int = 1000):
    """
    Stream content from Google Generative AI safely.
    Handles SDK exceptions and missing chunk.text.
    """
    try:
        response = model.generate_content(prompt, stream=True)
        for i, chunk in enumerate(response):
            if i >= max_chunks:
                yield "data: [Stream truncated]\n\n"
                break
            text = getattr(chunk, "text", None)
            if text:
                yield f"data: {text}\n\n"
    except Exception as e:
        yield f"data: [Error during AI streaming: {str(e)}]\n\n"


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json or {}
    message = data.get("message", "")
    history = data.get("history", [])
    prompt = build_prompt(message, history)
    return Response(stream_with_context(gemini_stream(prompt)), mimetype="text/event-stream")


@app.route("/stream", methods=["POST"])
def stream_raw_prompt():
    data = request.json or {}
    user_prompt = data.get("prompt", "")
    return Response(stream_with_context(gemini_stream(user_prompt)), mimetype="text/event-stream")


@app.route("/")
def home():
    return "Backend is running! Visit the API endpoints."


# -------------------------------
# Local Development
# -------------------------------
if __name__ == "__main__":
    create_db()
    with app.app_context():
        ensure_global_room()
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
