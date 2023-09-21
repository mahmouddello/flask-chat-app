// AJAX OPERATIONS
let ajax_login_post = (usernameVal, passwordVal) => {
    const data = {
        username: usernameVal, password: passwordVal
    };
    $.ajax({
        type: "POST",
        contentType: "application/json",
        url: "http://127.0.0.1:5000/authentication/login",
        data: JSON.stringify(data),
        dataType: "json",
        cache: false,
        timeout: 4000,
        success: function (data) {
            if (data.status) {
                customPopoutAlert("Login Success", "success")
                window.location.href = "http://127.0.0.1:5000/"
            } else {
                customPopoutAlert("Bad Credentials", "error")
            }
        },
        error: function (xhr) {
            customPopoutAlert("Alert" + xhr.status + "Check error code and try again", "error")
        }
    })
}

let ajax_register_post = (usernameVal, emailVal, passwordVal) => {
    const userData = {
        username: usernameVal,
        email: emailVal,
        password: passwordVal
    }

    $.ajax({
        type: "POST",
        contentType: "application/json",
        url: "http://127.0.0.1:5000/authentication/register",
        data: JSON.stringify(userData),
        dataType: "json",
        cache: false,
        timeout: 4000,
        success: function (data) {
            if (data.status) {
                customPopoutAlert("Registration Success," +
                    " Redirecting to the login page", "success")
                window.location.href = "http://127.0.0.1:5000/authentication/login"
            } else {
                customPopoutAlert("Username already has been taken by another user", "error")
            }
        },
        error: function (xhr) {
            customPopoutAlert("Error:" + xhr.status + "Check the error code and try again", "error")
        }
    });
}

let ajax_join_room_post = (room_id) => {
    const user_data = {
        "room_id": room_id
    }
    $.ajax({
        type: "POST",
        contentType: "application/json",
        url: "http://127.0.0.1:5000/chat/join_room",
        data: JSON.stringify(user_data),
        dataType: "json",
        cache: false,
        timeout: 4000,
        success: function (data) {
            if (data.status === "Joined") {
                customPopoutAlert("Joined Room Successfully.", "success")
                window.location.href = "http://127.0.0.1:5000/chat/my_rooms"
            } else if (data.status === "Already Room Member") {
                customPopoutAlert("You're already member of this room", "error")
            } else if (data.status === "No Room Found") {
                customPopoutAlert("Invalid Room Id", "error")
            }
        },
        error: function (xhr) {
            customPopoutAlert("Error:" + xhr.status + "Check the error code and try again", "error")
        }
    });
}

let ajax_create_room_post = (room_name) => {
    const user_data = {
        "room_name": room_name
    }
    $.ajax({
        type: "POST",
        contentType: "application/json",
        url: "http://127.0.0.1:5000/chat/create_room",
        data: JSON.stringify(user_data),
        dataType: "json",
        cache: false,
        timeout: 4000,
        success: function (data) {
            if (data.status) {
                customPopoutAlert("Created Room Successfully, Redirecting...", "success")
                window.location.href = "http://127.0.0.1:5000/chat/my_rooms"
            } else {
                customPopoutAlert("Failed to create room :(", "error")
            }
        },
        error: function (xhr) {
            customPopoutAlert("Error:" + xhr.status + "Check the error code and try again", "error")
        }
    });
}

let ajax_change_username = (new_username, password) => {
    const user_data = {
        "new_username": new_username,
        "password": password
    }
    $.ajax({
        type: "POST",
        contentType: "application/json",
        url: "http://127.0.0.1:5000/edit_credentials/change_username",
        data: JSON.stringify(user_data),
        dataType: "json",
        cache: false,
        timeout: 4000,
        success: function (data) {
            if (data.status === true) {
                customPopoutAlert("You've changed your username successfully! Redirecting to login page",
                    "success",
                    "#usernameAlert")
                window.location.href = "http://127.0.0.1:5000/authentication/login"
            } else if (data.status === "Duplicate") {
                customPopoutAlert("This username already has been taken, try different one!",
                    "error", "#usernameAlert")
            } else if (data.status === "Invalid Password") {
                customPopoutAlert("Invalid password, try again :(", "error", "#usernameAlert")
            } else {
                customPopoutAlert("An error occurred during writing to the database!",
                    "error", "#usernameAlert")
            }
        },
        error: function (xhr) {
            customPopoutAlert("Error:" + xhr.status + "Check the error code and try again",
                "error", "#usernameAlert")
        }
    });
}

let ajax_change_email = (new_email, password) => {
    const user_data = {
        "new_email": new_email,
        "password": password
    }
    $.ajax({
        type: "POST",
        contentType: "application/json",
        url: "http://127.0.0.1:5000/edit_credentials/change_email",
        data: JSON.stringify(user_data),
        dataType: "json",
        cache: false,
        timeout: 4000,
        success: function (data) {
            if (data.status === true) {
                customPopoutAlert("You've changed your email successfully! Redirecting to login page",
                    "success",
                    "#emailAlert")
                window.location.href = "http://127.0.0.1:5000/authentication/login"
            } else if (data.status === "Same Email") {
                customPopoutAlert("You can't change your email to the same email! try different one!",
                    "error",
                    "#emailAlert")
            } else {
                customPopoutAlert("Either password is incorrect or an error occurred during writing to the database!" +
                    ", try again later", "error", "#emailAlert")
            }
        },
        error: function (xhr) {
            customPopoutAlert("Error:" + xhr.status + "Check the error code and try again",
                "error", "#emailAlert")
        }
    });
}

let ajax_change_password = (old_password, new_password) => {
    const user_data = {
        "old_password": old_password,
        "new_password": new_password
    }
    $.ajax({
        type: "POST",
        contentType: "application/json",
        url: "http://127.0.0.1:5000/edit_credentials/change_password",
        data: JSON.stringify(user_data),
        dataType: "json",
        cache: false,
        timeout: 4000,
        success: function (data) {
            if (data.status === true) {
                customPopoutAlert(
                    "Password has been changed successfully! Redirecting to login page",
                    "success",
                    "#passwordAlert")
                window.location.href = "http://127.0.0.1:5000/authentication/login"
            } else if (data.status === "Same Password") {
                customPopoutAlert(
                    "You can't change your password to the existed one, try different password!",
                    "error",
                    "#passwordAlert")
            } else if (data.status === "Invalid Password") {
                customPopoutAlert(
                    "Invalid Password, check your password and try again!",
                    "error",
                    "#passwordAlert")
            } else {
                customPopoutAlert(
                    "An error occurred, try again later!",
                    "error",
                    "#passwordAlert")
            }
        },
        error: function (xhr) {
            customPopoutAlert("Error:" + xhr.status + "Check the error code and try again",
                "error", "#passwordAlert")
        }
    });
}

let ajax_leave_room = (button) => {
    const room_id = button.getAttribute("data-room-id");
    const username = button.getAttribute("data-username");
    const user_data = {
        "room_id": room_id,
        "username": username
    };
    $.ajax({
        type: "POST",
        contentType: "application/json",
        url: "http://127.0.0.1:5000/chat/leave_room",
        data: JSON.stringify(user_data),
        dataType: "json",
        cache: false,
        timeout: 4000,
        success: function (data) {
            if (data.status) {
                customPopoutAlert("Leaved Room Successfully", "success")
                window.location.href = "http://127.0.0.1:5000"
            } else {
                customPopoutAlert("Failed to leave", "error")
            }
        }
    });
}