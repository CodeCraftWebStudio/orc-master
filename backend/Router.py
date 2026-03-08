###################################################################################################################
#   ROUTER.PY
#   THE CENTER OF BACKEND OPERATIONS
###################################################################################################################

from .models.model_base.events_model import CalendarEvent
from backend.models.model_base.user_services.services import check_if_a_user_has_logged_in_with_a_role
from backend.models.model_base.user_services.services import (
    get_user_by_key,
    register_user,
    check_if_a_user_has_logged_in_with_a_role
)
from backend.models.model_base.user_services.executive_base import EXECUTIVE_ROLES
import os
from flask import Flask, jsonify, redirect, request, Response, stream_with_context
from functools import wraps
from .error_messages.errors import ValidationError, AuthenticationError, AuthorizationError, NotFoundError, ensure_requirements,  session_key_required
from .Database import app
from .local_storage import localStorage
from cryptography.fernet import Fernet
from backend.models.model_base.user_services.services import create_anonymous_user, get_user_by_key, check_user_registered_from_user, check_user_registered_from_session_key, check_if_a_user_has_logged_in_with_a_role, User
from backend.models.security import generate_secret_key, reversible_dehasher, reversible_hasher
from backend.models.model_base.user_services.services import get_total_user_count, RoleType, db, get_all_contacts
from backend.learn.config import generate_quiz
from datetime import datetime
from backend.models.model_base.general_base import create_db
from backend.chatroom.Models.room import Room
from backend.chatroom.Models.message import Message
from backend.chatroom.Services.professional import SYSTEM_INSTRUCTIONS, ask_red
from flask_socketio import SocketIO, emit, join_room, leave_room
from backend.models.secret_key_generator import api
import google.generativeai as genai


LOCAL_STORAGE = localStorage()
GET, POST, UPDATE, DELETE = "GET", "POST", "UPDATE", "DELETE"
SECRET_KEY = LOCAL_STORAGE.getItem('ORC')
socketio = SocketIO(app, cors_allowed_origins="*", manage_session=False)

# -------------------------------------------------
# INITIALIZE DATABASE + ROOMS AT APP STARTUP
# -------------------------------------------------
with app.app_context():
    create_db()

    # Ensure required chat rooms exist
    if not Room.query.filter_by(name="global").first():
        db.session.add(Room(name="global"))

    if not Room.query.filter_by(name="executives").first():
        db.session.add(Room(name="executives"))

    db.session.commit()
# -------------------------------------------------


try:
    print(Fernet(SECRET_KEY))
except Exception as e:
    print(
        f"An error occured with the secret key {SECRET_KEY}. Apparently it isn't valid(I think). Error: {e}")
    SECRET_KEY = "Xh84PtDmGYycPnlLCyPLBVYBzpUZbPJdA2t2zxJhZKQ=".encode("utf-8")
    print(f"Forced secret key to be {SECRET_KEY}")


def hash_text(text):
    return reversible_hasher(text, SECRET_KEY)


def dehash_text(text):
    return reversible_dehasher(text, SECRET_KEY)


@app.route('/api/user/start', methods=[GET, POST])
def start_user_session():
    user = create_anonymous_user()
    if not user:
        return jsonify({"error": "user not found"}), 404
    elif not user.session_key:
        return jsonify({"error": "session key invalid or not found"}), 404
    return jsonify({"session_key": reversible_hasher(user.session_key, SECRET_KEY)})


@app.route('/api/user/getTotalMembers', methods=[GET])
def get_total_members():
    return jsonify(get_total_user_count())


@app.route('/api/user/getIsUserRegistered', methods=[POST])
def get_user_registered():
    data = request.get_json()
    session_key = data.get("session_key")
    if not session_key:
        print("No session key")
        return jsonify({"error": "session key not given"})
    user = get_user_by_key(session_key)
    if user:
        print(f"User found with the session key: {session_key}")
        print("User is found")
        if user.name not in ["Anonymous", "Unassigned"] and user.role_type != RoleType.GUEST:
            print(f"Username: {user.name} Roletype: {user.role_type}")
            return jsonify({"result": "t"})
        else:
            return jsonify({"result":  "f"})
    else:
        print("No user; user is not found")
        return jsonify({"error": "Invalid request"}), 400


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

    role_name = data["role_name"]
    role_code = data["role_code"]

    if role_name not in EXECUTIVE_ROLES:
        return jsonify({"error": "Invalid role"}), 400

    role_meta = EXECUTIVE_ROLES[role_name]

    if role_meta["code"] != role_code:
        return jsonify({"error": "Invalid code for selected role"}), 403

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
    if not data:
        return jsonify({"error": "No JSON body provided"})
    page_text = data.get("pageText")
    difficulty = data.get("difficulty")
    session_key = data.get("session_key")

    if not page_text or not difficulty or not session_key:
        return jsonify({"error": "Missing required fields"}), 400

    if len(page_text) > 20_000:
        return jsonify({"error": "Text too long"}), 413

    user = get_user_by_key(reversible_dehasher(
        data["session_key"], SECRET_KEY))
    if not user:
        return jsonify({"error": "Invalid session key"})
    new_key = user.rotate_key()
    result = generate_quiz(data["difficulty"], data["pageText"])
    quiz_json = result.parsed
    return jsonify({"result": quiz_json, "session_key": reversible_hasher(user.session_key, SECRET_KEY)})


@app.route('/api/user/getUserDetails', methods=[POST])
def get_user_details():
    data = request.get_json()
    session_key = data.get("session_key")
    if not session_key:
        return jsonify({"error": "No session key provided"})
    user = get_user_by_key(session_key)
    if not user:
        return jsonify({"error": "Invalid session key"})

    return jsonify({
        'name': user.name,
        'school_class': user.school_class,
        'role_type': user.role_type,
        'role_title': user.role_title
    })


@app.route('/api/tools/getHashedValue', methods=[POST])
def get_hashed_value():
    data = request.get_json()
    if not data.get("value"):
        return jsonify({"error": "Invalid input"})
    return jsonify({"result": hash_text(data.get("value"))})


@app.route('/api/tools/getDehashedValue', methods=[POST])
def get_dehashed_value():
    data = request.get_json()
    if not data.get("value"):
        return jsonify({"error": "Invalid input"})
    return jsonify({"result": dehash_text(data.get("value"))})


# Configure Gemini once at startup
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


def gemini_stream(prompt: str):
    response = model.generate_content(prompt, stream=True)
    for chunk in response:
        if chunk.text:
            yield f"data: {chunk.text}\n\n"


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json or {}
    message = data.get("message", "")
    history = data.get("history", [])

    prompt = build_prompt(message, history)

    return Response(
        stream_with_context(gemini_stream(prompt)),
        mimetype="text/event-stream",
    )


@app.route("/stream", methods=["POST"])
def stream_raw_prompt():
    data = request.json or {}
    user_prompt = data.get("prompt", "")

    return Response(
        stream_with_context(gemini_stream(user_prompt)),
        mimetype="text/event-stream",
    )


# -------------------------------------------------
# LOCAL DEVELOPMENT ONLY
# -------------------------------------------------
if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
