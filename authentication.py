from flask import Blueprint, render_template, request, redirect, url_for, jsonify, Response
from flask_login import login_user, logout_user, current_user, login_required

from database import get_user, save_user

authentication: Blueprint = Blueprint("authentication", __name__, url_prefix="/authentication")


@authentication.route(rule="/login/", methods=["GET", "POST"])
def login() -> Response | str:
    """
     Manages the login operation logic, handling both GET and POST requests,
     and redirects authenticated users to the home page.

    :return: HTML Template or Response.
    """
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    if request.method == "POST":
        data = request.get_json(force=True)
        username = data.get("username")
        password = data.get("password")
        user_object = get_user(username)  # get the user object by username
        if user_object and user_object.check_password(password_input=password):
            login_user(user_object)
            response_data = {
                "status": True,
                "message": "Login Success!",
                "redirectUrl": url_for("home")
            }
        else:
            response_data = {
                "status": False,
                "message": "Bad Credentials"
            }
        return jsonify(response_data)
    return render_template("login.html")


@authentication.route(rule="/register/", methods=["GET", "POST"])
def register() -> Response | str:
    """
    Handles the registration operation logic, including GET and POST requests,
    and redirects authenticated users to the home page.

    :return: HTML Template or Response.
    """
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    if request.method == "POST":
        data = request.get_json(force=True)
        username = data.get("username")
        email = data.get("email")
        password_input = data.get("password")
        return save_user(username=username, email=email, password=password_input)
    return render_template("register.html")


@authentication.route(rule="/logout")
@login_required
def logout() -> Response:
    """
    Logs out the user and redirects them to the home page; requires user authentication.

    :return: Response
    """
    logout_user()
    return redirect(url_for("home"))
