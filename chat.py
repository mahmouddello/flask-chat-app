from bson import ObjectId
from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user, login_required
from database import get_rooms_for_user, get_room, get_messages, get_room_members, join_room_member, save_room

chat = Blueprint("chat", __name__, url_prefix="/chat")


@chat.route("/my_rooms")
@login_required
def my_rooms() -> str:
    return render_template(
        template_name_or_list="my_rooms.html",
        logged_in=current_user.is_authenticated,
        rooms=get_rooms_for_user(username=current_user.username)
    )


@chat.route("/my_rooms/<room_id>")
@login_required
def view_room(room_id: ObjectId) -> str:
    room = get_room(room_id)
    messages = get_messages(room_id)
    return render_template(
        "view_room.html",
        room=room,
        logged_in=current_user.is_authenticated,
        messages=messages,
        username=current_user.username
    )


@chat.route("/join_room", methods=["POST"])
def join_room():
    data = request.get_json(force=True)
    room_id = data.get("room_id")
    room = get_room(room_id)
    try:
        room_name = room["name"]
    except TypeError:
        return jsonify({"status": "No Room Found"})  # handle room not found
    else:
        room_members = get_room_members(room_id=room_id)
        room_members = [member["_id"]["username"] for member in room_members]
        if current_user.username in room_members:
            print("He is already user")
            return jsonify({"status": "Already Room Member"})
        join_room_member(room_id=room_id, username=current_user.username, room_name=room_name)


@chat.route("/create_room", methods=["POST"])
def create_room():
    data = request.get_json(force=True)
    room_name = data.get("room_name")
    try:
        save_room(room_name=room_name, created_by=current_user.username)
    except Exception as e:
        print(e)
        return jsonify({"status": False})
    else:
        return jsonify({"status": True})
