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