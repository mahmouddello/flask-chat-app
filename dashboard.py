from flask import Blueprint, request, jsonify, Response
from flask_login import current_user
from database import db_change_username, db_change_email, db_change_password, get_user

dashboard_operations = Blueprint("dashboard_operations", __name__, url_prefix="/edit_credentials")


@dashboard_operations.route(rule="/change_username", methods=["POST"])
def change_username() -> Response:
    user_object = get_user(current_user.username)
    data = request.get_json(force=True)
    new_username = data.get("new_username")
    password = data.get("password")
    if user_object.check_password(password_input=password):
        return db_change_username(old_username=user_object.username, new_username=new_username)
    return jsonify({"status": "Invalid Password"})


@dashboard_operations.route(rule="/change_email", methods=["POST"])
def change_email() -> Response:
    user_object = get_user(current_user.username)
    data = request.get_json(force=True)
    new_email = data.get("new_email")
    password = data.get("password")

    if user_object.email == new_email:
        return jsonify({"status": "Same Email"})

    if user_object.check_password(password_input=password):
        return db_change_email(username=user_object.username, new_email=new_email)
    return jsonify({"status": False})


@dashboard_operations.route(rule="/change_password", methods=["POST"])
def change_password():
    user_object = get_user(current_user.username)
    data = request.get_json(force=True)
    old_password = data.get("old_password")
    new_password = data.get("new_password")

    # Same Password
    if old_password == new_password:
        return jsonify({"status": "Same Password"})

    if not user_object.check_password(password_input=old_password):
        return jsonify({"status": "Invalid Password"})

    return db_change_password(username=user_object.username, new_password=new_password)
