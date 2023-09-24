import os
from datetime import datetime
from functools import wraps
from typing import Callable, Any
from random import choice
from flask import jsonify, Response, abort, url_for
from flask_login import current_user, logout_user
from pymongo.mongo_client import MongoClient
from pymongo.errors import DuplicateKeyError, PyMongoError
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
from user import User

load_dotenv("./.env")  # .env file

uri = os.getenv("MONGODB_URI")

# Create a new client and connect to the server
client = MongoClient(uri)

# database
chat_db = client.get_database("ChatDB")

# collections: tables
users_collection = chat_db.get_collection("users")
rooms_collection = chat_db.get_collection("rooms")
room_members_collection = chat_db.get_collection("room_members")
messages_collection = chat_db.get_collection("messages")
sequences_collection = chat_db.get_collection("sequences")

# indexes
users_collection.create_index([("username", 1)], unique=True)


# User Operations
def get_user(username: str) -> User | None:
    """
    Gets the data of user from the database by unique `_id` (MongoDB Default ID) which is username.
    :param username: Username sent from the form
    :returns: User Object
    :rtype: User or None
    """
    user_data = users_collection.find_one({"username": username})
    return User(username=user_data["username"], email=user_data["email"],
                password=user_data["password"]) if user_data else None


def save_user(username: str, email: str, password: str) -> Response:
    """
    Saves a user to database.

    :param username: username of the user that will be created.
    :param email: email of the user that will be created.
    :param password: password of the user that will be created.
    :return: Response
    """
    try:
        users_collection.insert_one({
            "username": username,
            "email": email,
            "password": generate_password_hash(password)

        })
    except DuplicateKeyError:
        return jsonify({
            "status": False,
            "message": "Username has already been taken! try different one"
        })

    else:
        logout_user()
        return jsonify({
            "status": True,
            "message": "Registration Success! Redirecting to the login page",
            "redirectUrl": url_for("authentication.login")
        })


def db_change_username(old_username: str, new_username: str) -> Response:
    """
    Updates the username of the current user in the database.

    :param old_username: current user's username
    :param new_username: The new username to set for the current user.
    :type old_username: str    :type new_username: str

    :returns: A Response object indicating the status of the username update.
    :rtype: Response
    """
    try:
        # Update the username in the users_collection
        users_collection.update_one(
            {"username": old_username},
            {"$set": {"username": new_username}},
        )

        # Update the username in the room_members collection where added_by matches the old username
        room_members_collection.update_many(
            {"$and": [{"username": old_username}, {"added_by": old_username}]},
            {"$set": {"username": new_username, "added_by": new_username}},
        )

        # Update the username in the rooms collection
        rooms_collection.update_many(
            {"created_by": old_username},
            {"$set": {"created_by": new_username}},
        )

        # Update the sender information in messages collection
        messages_collection.update_many(
            {"sender": old_username},
            {"$set": {"sender": new_username}}
        )

    except DuplicateKeyError:
        return jsonify({
            "status": False,
            "message": "This username already in use, try different one!",
            "alertDiv": "#usernameAlert"
        })

    except PyMongoError:
        return jsonify({
            "status": False,
            "message": "An error occurred when writing to the database, try again later!",
            "alertDiv": "#usernameAlert"
        })

    else:
        logout_user()
        return jsonify({
            "status": True,
            "message": "Changed username successfully",
            "alertDiv": "#usernameAlert",
            "redirectUrl": url_for("home")
        })


def db_change_email(username: str, new_email: str) -> Response:
    """
    Updates the username of the current user in the database.

    :param username:  current user's username
    :param new_email: The new email to set for the current user.
    :type new_email: str

    :returns: A Response object indicating the status of the email update.
    :rtype: Response
    """
    try:
        users_collection.update_one(
            {"username": username},
            {"$set": {"email": new_email}}
        )
    except PyMongoError:
        return jsonify({
            "status": False,
            "message": "An error occurred, try again later!",
            "alertDiv": "#emailAlert"
        })

    else:
        logout_user()
        return jsonify({
            "status": True,
            "redirectUrl": url_for("home")
        })


def db_change_password(username: str, new_password: str) -> Response:
    """
    Updates the password of the current user in the database.

    :param username: current user's username
    :param new_password: user's new password

    :return: A Response object indicating the status of the password update.
    :rtype: Response
    """
    try:
        users_collection.update_one(
            {"username": username},
            {"$set": {"password": generate_password_hash(new_password)}}
        )
    except PyMongoError:
        return jsonify({
            "status": False,
            "alertDiv": "#passwordAlert",
            "message": "An error occurred, try again later!"
        })

    else:
        logout_user()
        return jsonify({
            "status": True,
            "redirectUrl": url_for("home")
        })


def is_room_member(room_id: int, username: str) -> int:
    """
    Checks for if the current user is member of the room that he want to view and text into.

    :param room_id: room id fetched from the link in my_rooms.html template
    :param username: current user's username.
    :return: Integer state which represent boolean value (0 or 1).
    """
    return room_members_collection.count_documents({'room_id': room_id, 'username': username})


def is_admin(room_id: int, username: str) -> int:
    """
    Checks if the user is admin.

    :param room_id: room's id.
    :param username: current user's username.
    :return: Boolean state of 0 or 1 (True or False)
    """
    return room_members_collection.count_documents({
        "room_id": room_id,
        "username": username,
        "is_room_admin": True
    })


def admin_required(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator to prevent accessing some routes for non-admin users.
    :param func: Decorated function
    :return: Callable[..., Any]
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        room_id = kwargs.get("room_id")
        username = current_user.username  # Assuming you have access to the current user's username

        # Check if the user is an admin for the specified room
        if not is_admin(room_id, username):
            return abort(403)  # Return a forbidden (403) error if the user is not an admin

        return func(*args, **kwargs)

    return wrapper


def delete_room_member(room_id: int, username: str) -> Response:
    """
    Deletes member from a room, if he is admin and there is other members in the room; it transfers admin abilities
    to a random user. if he is the only member in the room and the admin leaves, the room also get deleted.

    :param room_id: current room's id.
    :param username: current logged-in user's username.
    :return: Response
    """
    try:
        # Check if the user is an admin
        if is_admin(room_id, username):
            room_members = get_room_members(room_id)

            # Delete non-admin members
            room_members = [member["username"] for member in room_members if not member["is_room_admin"]]
            if room_members:
                new_admin = choice(room_members)
                room_members_collection.update_one(
                    {'room_id': room_id, "username": new_admin},
                    {'$set': {"is_room_admin": True}}
                )
            else:
                # Delete the room because no members left
                rooms_collection.delete_one({"room_id": room_id})

        # Delete the user
        room_members_collection.delete_one({"room_id": room_id, "username": username})

        return jsonify({
            "status": True,
            "message": "Leaved Room Successfully",
            "redirectUrl": url_for("chat.my_rooms")
        })
    except PyMongoError:
        return jsonify({
            "status": False,
            "message": "Failed to leave!"
        })


def db_kick_member(room_id: int, username: str) -> Response:
    """
    Responsible about kicking user from the room.

    :param room_id: selected room's id.
    :param username: current user's (admin) username.
    :return: Response
    """
    try:
        room_members_collection.delete_one({
            "room_id": room_id, "username": username
        })
    except PyMongoError:
        return jsonify({"status": False})
    else:
        return jsonify({"status": True})


# Room Operations

def get_room(room_id: int) -> dict:
    """
    Find a room by `room_id`

    :param room_id: fetched id for the room.
    :type room_id: int
    :return: Dictionary (JSON) object contains room data.
    """
    return rooms_collection.find_one({'room_id': room_id})


def save_room(room_name: str, created_by: str) -> int:
    """
    Allows a user to create a room, giving them admin access and automatically adding them to the room.

    :param room_name: The name of the room to be created.
    :param created_by: The username of the user who is creating the room.
    :type room_name: str,
    :type created_by: str

    :return: Created Room's ID.
    """
    room_id = get_next_sequence_value("room_id")
    rooms_collection.insert_one({
        "room_id": room_id,
        "name": room_name,
        "created_by": created_by,
        "created_at": datetime.now()
    })
    add_room_member(room_id, room_name=room_name, username=created_by, added_by=created_by, is_room_admin=True)
    return room_id


def add_room_member(room_id: int, room_name: str, username: str, added_by, is_room_admin=False):
    """
    Add a member to a room with `room_id`.

    :param room_id: The id of the room to which the member will be added.
    :param room_name: The name of the room.
    :param username: The username of the member to be added.
    :param added_by: The username of the user who is adding the member (default is "Himself").
    :param is_room_admin: Whether the member should have admin privileges in the room (default is False).
    :return:
    """
    room_members_collection.insert_one(
        {"room_id": room_id, 'username': username, 'room_name': room_name, 'added_by': added_by,
         'added_at': datetime.now(), 'is_room_admin': is_room_admin})


def get_rooms_for_user(username: str) -> list:
    """
    Returns a list of rooms for the current signed-in user.

    :param username: The username of the user.
    :return: A list of rooms the user is a member of.
    """
    return list(room_members_collection.find({'username': username}))


def get_room_members(room_id: int) -> list:
    """
    Returns a list of members for a room.

    :param room_id: The id of the room.
    :return: A list of room members.
    """
    return list(room_members_collection.find({'room_id': room_id}))


def join_room_member(room_id: int, room_name: str, username: str, added_by="Himself",
                     is_room_admin=False) -> Response:
    """
    Responsible for joining a room by room_id, handling this operation on the join room modal.

    :param room_id: The id of the room to join.
    :param room_name: The name of the room.
    :param username: The username of the user joining the room.
    :param added_by: The username of the user who is added the member (default is "Himself").
    :param is_room_admin: Whether the member should have admin privileges in the room (default is False).
    :return: Response
    """
    room_members_collection.insert_one(
        {'room_id': room_id, 'username': username, 'room_name': room_name, 'added_by': added_by,
         'added_at': datetime.now(), 'is_room_admin': is_room_admin})
    room_members = get_room_members(room_id=room_id)
    room_members = [member["username"] for member in room_members]
    if current_user.username in room_members:
        return jsonify({
            "status": True,
            "message": "Joined Room Successfully",
            "redirectUrl": url_for("chat.my_rooms")
        })


def get_next_sequence_value(sequence_name: str) -> int:
    """
    Gets the last sequential value of the sequence name from the collection and increment it by 1.
    :param sequence_name:
    :return: The incremented sequential value.
    """
    sequence_doc = sequences_collection.find_one_and_update(
        {"_id": sequence_name},
        {"$inc": {"sequence_value": 1}},
        return_document=True
    )
    return sequence_doc["sequence_value"]


def db_change_room_name(room_id: int, new_room_name: str) -> Response:
    """
    Change room's name in the database.
    :param room_id: room's id.
    :param new_room_name: new room name to be set.
    :return: Response
    """
    try:
        # Rooms collection
        rooms_collection.find_one_and_update(
            {"room_id": room_id},
            {"$set": {"name": new_room_name}}
        )

        # Room members collection
        room_members_collection.update_many(
            {"room_id": room_id},
            {"$set": {"room_name": new_room_name}}
        )
    except PyMongoError:
        return jsonify({
            "status": False,
            "message": "Failed to change room name!"
        })

    else:
        return jsonify({
            "status": True,
            "message": "Changed Room name successfully!",
            "redirectUrl": url_for("chat.view_room", room_id=room_id)
        })


# Messages

def get_messages(room_id: int) -> list:
    """
    Returns a list of messages for the selected room.

    :param room_id: The id of the room.
    :return: A list of messages in the room.
    """
    return list(messages_collection.find({"room_id": room_id}))


def save_message(room_id: int, text: str, sender: str) -> None:
    """
    Save a message to the database after emitting an event of SocketIO.

    :param room_id:  The id of the room where the message is sent.
    :param text: The content of the message.
    :param sender: The username of the message sender.
    :return: None
    """
    messages_collection.insert_one({
        "room_id": room_id,
        "text": text,
        "sender": sender,
        "create_at": datetime.now()
    })
