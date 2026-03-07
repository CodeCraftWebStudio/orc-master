from ..user_model import User
from ..general_base import db, RoleType
import secrets
from ...security import reversible_dehasher, reversible_hasher
from ....local_storage import localStorage as LOCAL_STORAGE
from ..events_model import CalendarEvent
from datetime import datetime
from ....error_messages.errors import *
from ....chatroom.Models.models import Room as Contact
localStorage = LOCAL_STORAGE()
SECRET_KEY = localStorage.getItem('ORC')
# sprint(SECRET_KEY)
def create_anonymous_user():
    user = User(  
        session_key=secrets.token_hex(32)
    )
    db.session.add(user)
    db.session.commit()
    return user 
def get_user_by_key(session_key):
    try:
        print("Trying in case key is hashed")
        user = User.query.filter_by(session_key=reversible_dehasher(session_key, SECRET_KEY),is_active=True).first()
        return user
    except Exception as e:
        print(f"It appears something went wrong: {e}")
        try:
            print("Checking to see if the user hasn't hashed their key")
            user = User.query.filter_by(session_key=session_key,is_active=True).first()
            return user
        except Exception as e:
            print(f"It seems there's an error: {e}")
            return None
def get_user_from_key(session_key):
    return get_user_by_key(session_key)
def rotate_and_commit(user: User):
    user.rotate_key()
    db.session.commit()
    return user.session_key

def register_user(user: User, name, school_class):
    user.name = name
    user.school_class = school_class
    user.role_type = RoleType.MEMBER
    user.rotate_key()
    db.session.commit()

def assign_role(president, target_user, role_type, role_title=None):
    if president.role_type != RoleType.ADMIN:
        raise PermissionError("Only President/Admin can assign roles")

    target_user.role_type = role_type
    target_user.role_title = role_title
    db.session.commit()

def resign_role(user: User):
    if user.role_type == RoleType.ADMIN:
        raise PermissionError("The President cannot resign unless they appoint another person to take their place.")
    user.role_type = RoleType.MEMBER
    user.role_title = None
    user.rotate_key()
    db.session.commit()

def logout_user(user):
    user.session_key = None
    user.is_active = False
    db.session.commit()

def get_total_user_count():
    return db.session.query(User).count()

def get_all_users():
    return db.session.query(User).all()
def get_all_contacts():
    users = get_all_users()
    contacts = []

    for user in users:
        if user.role_type not in [RoleType.GUEST]:
            contacts.append({
                "id": user.id,
                "username": user.name,
                "role": user.role_title
            })

    return contacts
def check_user_registered_from_session_key(hashed_session_key, secret_key=SECRET_KEY):
    user = get_user_from_key(reversible_dehasher(hashed_session_key, secret_key))
    if not user:
        print("User not found")
        return False
    if user.role_type == RoleType.GUEST:
        print("User is a guest")
        return False
    else:
        print("User is a member")
        return True
def check_user_registered_from_user(user: User, secret_key=SECRET_KEY):
    return check_user_registered_from_session_key(user.session_key, secret_key)

def get_user_role_from_user(user: User):
    return user.role_type

def get_user_role_from_raw_session_key(session_key):
    return get_user_role_from_user(get_user_by_key(session_key))

def get_user_role_from_hashed_session_key(session_key):
    return get_user_role_from_raw_session_key(reversible_hasher(session_key))

def check_if_a_user_has_logged_in_with_a_role(given_role_title):
    answer = User.query.filter_by(role_title=given_role_title,is_active=True).first()
    if answer:
        return True
    return False

def create_event(date_obj=None, time_obj=None, description_obj=None):
    print(end="")
    if not date_obj:
        date_obj = datetime.now().date()
    if not time_obj:
        time_obj = "Variable time"
    if not description_obj:
        description_obj = "Red Cross Meeting"
    return  CalendarEvent().create(date_obj=date_obj, time_obj=time_obj, description_obj=description_obj)

def update_event(id, new_time, new_description):
    print(end="")
    if not id:
        return AuthorizationError("Cannot update event without id")
    event = CalendarEvent.query.filter_by(id=id).first()
    if not event:
        return AuthorizationError("Invalid id given")
    if not new_time:
        new_time = event.time
    if not new_description:
        new_description = event.description
    return event.update(id=id, new_time=new_time, new_description=new_description)


def delete_event(id):
    event = CalendarEvent.query.filter_by(id=id).first()
    if not event:
        return AuthorizationError("Invalid id given for event")
    event.delete(id=id)    

