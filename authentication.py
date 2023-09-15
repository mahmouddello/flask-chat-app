from flask import Blueprint, render_template, request, redirect, url_for, jsonify, Response
from flask_login import login_user, logout_user, current_user, login_required
from pymongo.errors import DuplicateKeyError
from database import get_user, save_user

authentication: Blueprint = Blueprint("authentication", __name__, url_prefix="/authentication")


@authentication.route(rule="/login", methods=["GET", "POST"])
def login() -> Response | str:
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    if request.method == "POST":
        try:
            data = request.get_json(force=True)
            username = data.get("username")
            password = data.get("password")
            user_object = get_user(username)  # get the user object by username
            if user_object and user_object.check_password(password_input=password):
                login_user(user_object)
                return jsonify({"status": True})
            else:
                return jsonify({"status": False})
        except Exception as e:
            print(e)
            return jsonify({"status": False})
    return render_template("login.html")


@authentication.route(rule="/register", methods=["GET", "POST"])
def register() -> Response | str:
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    if request.method == "POST":
        try:
            data = request.get_json(force=True)
            username = data.get("username")
            email = data.get("email")
            password_input = data.get("password")
            try:
                save_user(username=username, email=email, password=password_input)
            # user already exists
            except DuplicateKeyError:
                return jsonify({"status": False})
            # return true status, then redirect to the login page from js.
            else:
                return jsonify({"status": True})
        except Exception as e:
            print(e)
    return render_template("register.html")


@authentication.route(rule="/logout")
@login_required
def logout() -> Response:
    logout_user()
    return redirect(url_for("home"))
