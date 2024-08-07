from flask import Blueprint, render_template, request, jsonify, Response, abort, url_for
from flask_login import current_user, login_required
from pymongo.errors import PyMongoError

from database import (
    get_rooms_for_user, get_room, get_messages, get_room_members,
    join_room_member, save_room, is_room_member, is_admin, admin_required, delete_room_member, db_kick_member,
    db_change_room_name
)

chat = Blueprint("chat", __name__, url_prefix="/chat")


@chat.route(rule="/my_rooms/")
@login_required
def my_rooms() -> str:
    """
    A Flask Route to view my_rooms.html template.

    :returns: Renders my_rooms.html template.
    :rtype: str
    """
    rooms = get_rooms_for_user(current_user.username)

    return render_template(
        template_name_or_list="my_rooms.html",
        logged_in=current_user.is_authenticated,
        rooms=rooms
    )


@chat.route(rule="/my_rooms/<int:room_id>")
@login_required
def view_room(room_id: int) -> str:
    """
    A Flask Route to view a chat room in a separate template.
    :param room_id: The chat room id fetched from my_rooms template.
    :type room_id: int

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
            username=current_user.username,
            is_user_admin=is_admin(room_id=room_id, username=current_user.username)
        )

    return abort(404)


@chat.route("/my_rooms/<int:room_id>/edit/", methods=["GET", "POST"])
@login_required
@admin_required
def edit_room(room_id: int) -> str | Response:
    if request.method == "POST":
        data = request.get_json(force=True)
        new_room_name = data.get("new_room_name")
        room_id = int(data.get("room_id"))
        print("REACHED PYTHON ROUTE")
        return db_change_room_name(room_id=room_id, new_room_name=new_room_name)

    room = get_room(room_id)
    room_members = get_room_members(room_id)
    return render_template(
        "edit_room.html",
        room=room,
        room_members=room_members,
        logged_in=current_user.is_authenticated)


@chat.route(rule="/join_room/", methods=["POST"])
@login_required
def join_room() -> Response:
    """
    Responsible about joining room logic, handles different exceptions;
    like if a user is already in this room, or the room id is invalid.

    :return: Response
    """
    data = request.get_json(force=True)
    room_id = int(data.get("room_id"))
    room = get_room(room_id)
    try:
        room_name = room["name"]
    except TypeError:
        return jsonify({
            "status": False,
            "message": "No Room Found!"
        })  # handle room isn't found

    room_members = get_room_members(room_id=room_id)
    room_members = [member["username"] for member in room_members]
    if current_user.username in room_members:
        return jsonify({
            "status": False,
            "message": "Already Room Member!"
        })

    return join_room_member(room_id=room_id, username=current_user.username, room_name=room_name)


@chat.route(rule="/create_room/", methods=["POST"])
@login_required
def create_room():
    """
    Responsible about creating room logic.

    :return: Response
    """
    data = request.get_json(force=True)
    room_name = data.get("room_name")
    try:
        save_room(room_name=room_name, created_by=current_user.username)
    except PyMongoError:
        return jsonify({
            "status": False,
            "message": "An error occurred when trying to write to the database!"})

    return jsonify({
        "status": True,
        "message": "Created Room Successfully :)",
        "redirectUrl": url_for("chat.my_rooms")
    })


@chat.route(rule="/leave_room/", methods=["POST"])
@login_required
def leave_room() -> Response:
    """
    Route to handle leave room functionality.
    :return: Response
    """
    data = request.get_json(force=True)
    print(data.get("room_id"))
    room_id = int(data.get("room_id"))
    username = data.get("username")

    return delete_room_member(room_id=room_id, username=username)


@chat.route(rule="/kick_member", methods=["POST"])
@admin_required
@login_required
def kick_member() -> Response:
    """
    Route to handle kicking member.
    :return: Response
    """
    data = request.get_json(force=True)
    room_id = int(data.get("room_id"))
    username = data.get("username")

    return db_kick_member(room_id=room_id, username=username)
