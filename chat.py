from bson import ObjectId
from flask import Blueprint, render_template, request, jsonify, Response, abort
from flask_login import current_user, login_required
from database import get_rooms_for_user, get_room, get_messages, get_room_members, join_room_member, save_room, \
    is_room_member

chat = Blueprint("chat", __name__, url_prefix="/chat")


@chat.route(rule="/my_rooms")
@login_required
def my_rooms() -> str:
    """
    A Flask Route to view my_rooms.html template.

    :returns: Renders my_rooms.html template.
    :rtype: str
    """
    return render_template(
        template_name_or_list="my_rooms.html",
        logged_in=current_user.is_authenticated,
        rooms=get_rooms_for_user(username=current_user.username)
    )


@chat.route(rule="/my_rooms/<room_id>")
@login_required
def view_room(room_id: ObjectId) -> str:
    """
    A Flask Route to view a chat room in a separate template.
    :param room_id: The chat room id fetched from my_rooms template.
    :type room_id: ObjectId

    :returns: Renders view_room.html template.
    :rtype: str
    """
    room = get_room(room_id)
    if room and is_room_member(room_id=room_id, username=current_user.username):
        messages = get_messages(room_id)
        return render_template(
            "view_room.html",
            room=room,
            logged_in=current_user.is_authenticated,
            messages=messages,
            username=current_user.username
        )
    abort(404)


@chat.route(rule="/join_room", methods=["POST"])
def join_room() -> Response:
    """
    Responsible about joining room logic, handles different exceptions;
    like if user is already in this room, or the room id is invalid.

    :return: Response
    """
    data = request.get_json(force=True)
    room_id = data.get("room_id")
    room = get_room(room_id)
    try:
        room_name = room["name"]
    except TypeError:
        return jsonify({"status": "No Room Found"})  # handle room not found
    else:
        room_members = get_room_members(room_id=room_id)
        room_members = [member["username"] for member in room_members]
        if current_user.username in room_members:
            return jsonify({"status": "Already Room Member"})
        return join_room_member(room_id=room_id, username=current_user.username, room_name=room_name)


@chat.route(rule="/create_room", methods=["POST"])
def create_room():
    """
    Responsible about creating room logic.

    :return: Response
    """
    data = request.get_json(force=True)
    room_name = data.get("room_name")
    try:
        save_room(room_name=room_name, created_by=current_user.username)
    except Exception as e:
        print(e)
        return jsonify({"status": False})
    else:
        return jsonify({"status": True})
