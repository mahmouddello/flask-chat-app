import os
from datetime import datetime
from bson import ObjectId
from flask import jsonify, Response
from flask_login import current_user
from pymongo.mongo_client import MongoClient
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


def get_user(username: str) -> User | None:
    """
    Gets the data of user from the database by unique `_id` (MongoDB Default ID) which is username.
    :returns: User or None
    """
    user_data = users_collection.find_one({"_id": username})
    return User(username=user_data["_id"], email=user_data["email"],
                password=user_data["password"]) if user_data else None


def save_user(username: str, email: str, password: str) -> None:
    """Save user to database, doesn't return anything."""
    users_collection.insert_one({
        "_id": username,  # primary key on mongo db
        "email": email,
        "password": generate_password_hash(password)

    })


# Room Operations

def get_room(room_id: ObjectId) -> dict:
    """Find a room by ```room_id```, auto generated id in the mongo db is saved in `Binary text JSON Format`,
    so we need to convert our string to a format of BSON to match with the ```_id``` attribute."""
    return rooms_collection.find_one({'_id': ObjectId(room_id)})


def save_room(room_name: str, created_by: str) -> ObjectId:
    """Allows user to create a room, giving him admin access and automatically add him to the room."""
    room_id = rooms_collection.insert_one({
        "name": room_name, "created_by": created_by, "created_at": datetime.now()
    }).inserted_id  # id property for the new room
    add_room_member(room_id=room_id, room_name=room_name, username=created_by, added_by=created_by, is_room_admin=True)
    return room_id


def add_room_member(room_id: ObjectId, room_name: str, username: str, added_by, is_room_admin=False):
    """Add a member to a room with `room_id`."""
    room_members_collection.insert_one(
        {'_id': {'room_id': ObjectId(room_id), 'username': username}, 'room_name': room_name, 'added_by': added_by,
         'added_at': datetime.now(), 'is_room_admin': is_room_admin})


def get_rooms_for_user(username: str) -> list:
    """Returns list of rooms for the current signed-in user."""
    return list(room_members_collection.find({'_id.username': username}))


def get_room_members(room_id: ObjectId) -> list:
    """Returns a list of members for a room."""
    return list(room_members_collection.find({'_id.room_id': ObjectId(room_id)}))


def join_room_member(room_id: ObjectId, room_name: str, username: str, added_by="Himself",
                     is_room_admin=False) -> Response:
    """Responsible for joining room functionality by room_id, handling this operation on join room modal."""
    room_members_collection.insert_one(
        {'_id': {'room_id': ObjectId(room_id), 'username': username}, 'room_name': room_name, 'added_by': added_by,
         'added_at': datetime.now(), 'is_room_admin': is_room_admin})
    room_members = get_room_members(room_id=room_id)
    room_members = [member["_id"]["username"] for member in room_members]
    if current_user.username in room_members:
        return jsonify({"status": "Joined"})


# Messages

def get_messages(room_id: ObjectId) -> list:
    """Returns list of messages for the selected room."""
    return list(messages_collection.find({"room_id": room_id}))


def save_message(room_id: ObjectId, text: str, sender: str):
    """Save message to the database after emitting event of SocketIO."""
    messages_collection.insert_one({
        "room_id": room_id,
        "text": text,
        "sender": sender,
        "create_at": datetime.now()
    })
