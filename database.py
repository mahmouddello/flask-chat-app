import os
from datetime import datetime
from bson import ObjectId
from flask import jsonify, Response
from flask_login import current_user, logout_user
from pymongo.mongo_client import MongoClient
from pymongo.errors import DuplicateKeyError
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
        return jsonify({"status": False})

    else:
        logout_user()
        return jsonify({"status": True})


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
        users_collection.update_one(
            {"username": old_username},
            {"$set": {"username": new_username}},
        )
    except DuplicateKeyError:
        return jsonify({"status": "Duplicate"})

    except Exception as e:
        print(e)
        return jsonify({"status": False})

    else:
        return jsonify({"status": True})


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
    except Exception as e:
        print(e)
        return jsonify({"status": False})

    else:
        logout_user()
        return jsonify({"status": True})


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
    except Exception as e:
        print(e)
        return jsonify({"status": False})

    else:
        logout_user()
        return jsonify({"status": True})


# Room Operations

def get_room(room_id: ObjectId) -> dict:
    """
    Find a room by `room_id`

    :param room_id: fetched id for the room.
    :type room_id: ObjectId
    :return: Dictionary (JSON) object contains room data.
    """
    return rooms_collection.find_one({'_id': ObjectId(room_id)})


def save_room(room_name: str, created_by: str) -> ObjectId:
    """
    Allows a user to create a room, giving them admin access and automatically adding them to the room.

    :param room_name: The name of the room to be created.
    :param created_by: The username of the user who is creating the room.
    :type room_name: str,
    :type created_by: str

    :return: Created Room's ID.
    """
    room_id = rooms_collection.insert_one({
        "name": room_name, "created_by": created_by, "created_at": datetime.now()
    }).inserted_id  # id property for the new room
    add_room_member(room_id=room_id, room_name=room_name, username=created_by, added_by=created_by, is_room_admin=True)
    return room_id


def add_room_member(room_id: ObjectId, room_name: str, username: str, added_by, is_room_admin=False):
    """
    Add a member to a room with `room_id`.

    :param room_id: The ObjectId of the room to which the member will be added.
    :param room_name: The name of the room.
    :param username: The username of the member to be added.
    :param added_by: The username of the user who is adding the member (default is "Himself").
    :param is_room_admin: Whether the member should have admin privileges in the room (default is False).
    :return:
    """
    room_members_collection.insert_one(
        {'_id': {'room_id': ObjectId(room_id), 'username': username}, 'room_name': room_name, 'added_by': added_by,
         'added_at': datetime.now(), 'is_room_admin': is_room_admin})


def get_rooms_for_user(username: str) -> list:
    """
    Returns a list of rooms for the current signed-in user.

    :param username: The username of the user.
    :return: A list of rooms the user is a member of.
    """
    return list(room_members_collection.find({'_id.username': username}))


def get_room_members(room_id: ObjectId) -> list:
    """
    Returns a list of members for a room.

    :param room_id: The ObjectId of the room.
    :return: A list of room members.
    """
    return list(room_members_collection.find({'_id.room_id': ObjectId(room_id)}))


def join_room_member(room_id: ObjectId, room_name: str, username: str, added_by="Himself",
                     is_room_admin=False) -> Response:
    """
    Responsible for joining a room by room_id, handling this operation on the join room modal.

    :param room_id: The ObjectId of the room to join.
    :param room_name: The name of the room.
    :param username: The username of the user joining the room.
    :param added_by: The username of the user who is adding the member (default is "Himself").
    :param is_room_admin: Whether the member should have admin privileges in the room (default is False).
    :return:
    """
    room_members_collection.insert_one(
        {'_id': {'room_id': ObjectId(room_id), 'username': username}, 'room_name': room_name, 'added_by': added_by,
         'added_at': datetime.now(), 'is_room_admin': is_room_admin})
    room_members = get_room_members(room_id=room_id)
    room_members = [member["_id"]["username"] for member in room_members]
    if current_user.username in room_members:
        return jsonify({"status": "Joined"})


# Messages

def get_messages(room_id: ObjectId) -> list:
    """
    Returns a list of messages for the selected room.

    :param room_id: The ObjectId of the room.
    :return: A list of messages in the room.
    """
    return list(messages_collection.find({"room_id": room_id}))


def save_message(room_id: ObjectId, text: str, sender: str) -> None:
    """
    Save a message to the database after emitting an event of SocketIO.

    :param room_id:  The ObjectId of the room where the message is sent.
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
