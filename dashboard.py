from flask import Blueprint, request, jsonify, Response
from flask_login import current_user
from database import db_change_username, db_change_email, db_change_password, get_user

dashboard_operations = Blueprint("dashboard_operations", __name__, url_prefix="/edit_credentials")


@dashboard_operations.route(rule="/change_username/", methods=["POST"])
def change_username() -> Response:
    """
    Accepts a POST request to change a user's username,
    validates the provided password, and updates the username if valid.

    :return: Response
    """
    user_object = get_user(current_user.username)
    data = request.get_json(force=True)
    new_username = data.get("new_username")
    password = data.get("password")
    if user_object.check_password(password_input=password):
        return db_change_username(old_username=user_object.username, new_username=new_username)
    return jsonify({
        "status": False,
        "message": "Invalid Password!",
        "alertDiv": "#usernameAlert"
    })


@dashboard_operations.route(rule="/change_email/", methods=["POST"])
def change_email() -> Response:
    """
    Handles a POST request to update a user's email address, checks for the same email,
    validates the password, and updates the email if conditions are met.

    :return: Response
    """
    user_object = get_user(current_user.username)
    data = request.get_json(force=True)
    new_email = data.get("new_email")
    password = data.get("password")

    if user_object.email == new_email:
        return jsonify({
            "status": False,
            "message": "You can't change your email to your existing one!",
            "alertDiv": "#emailAlert"
        })

    if user_object.check_password(password_input=password):
        return db_change_email(username=user_object.username, new_email=new_email)
    return jsonify({
        "status": False,
        "message": "Invalid Password!",
        "alertDiv": "#emailAlert"
    })


@dashboard_operations.route(rule="/change_password/", methods=["POST"])
def change_password() -> Response:
    """
    Manages a POST request to modify a user's password, checks for the same password,
    validates the old password, and updates it if criteria are satisfied.

    :return: Response
    """
    user_object = get_user(current_user.username)
    data = request.get_json(force=True)
    old_password = data.get("old_password")
    new_password = data.get("new_password")

    # Same Password
    if old_password == new_password:
        return jsonify({
            "status": False,
            "message": "You can't change your password to the existing one!",
            "alertDiv": "#passwordAlert"
        })

    if not user_object.check_password(password_input=old_password):
        return jsonify({
            "status": False,
            "message": "Invalid Password!",
            "alertDiv": "#passwordAlert"
        })

    return db_change_password(username=user_object.username, new_password=new_password)
