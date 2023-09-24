function makeAjaxRequest(type, url, data, successCallback, errorCallback) {
    const ajaxSettings = {
        type: type,
        contentType: "application/json",
        url: url,
        data: JSON.stringify(data),
        dataType: "json",
        cache: false,
        timeout: 4000,
        success: successCallback,
        error: errorCallback,
    };

    $.ajax(ajaxSettings);
}

function handleSuccess(data) {
    const redirectUrl = data["redirectUrl"]
    const alertDiv = data["alertDiv"] !== null && data["alertDiv"] !== undefined ? data["alertDiv"] : "#alert";
    if (data.status) {
        customPopoutAlert(data.message, "success", alertDiv);
        if (redirectUrl) {
            window.location.href = redirectUrl;
        }
    } else {
        customPopoutAlert(data.message, "error", alertDiv);
    }
}

function handleError(xhr) {
    const alertDiv = xhr["alertDiv"] !== null ? xhr["alertDiv"] : "#alert";
    customPopoutAlert(`Error: ${xhr.status} - Check the error code and try again`, "error", alertDiv);
}

function ajaxLogin(usernameVal, passwordVal) {
    const userData = {
        username: usernameVal,
        password: passwordVal
    }

    makeAjaxRequest(
        "POST",
        "http://127.0.0.1:5000/authentication/login",
        userData,
        handleSuccess,
        handleError
    );
}

function ajaxRegister(usernameVal, emailVal, passwordVal) {
    const userData = {
        username: usernameVal,
        email: emailVal,
        password: passwordVal
    }

    makeAjaxRequest(
        "POST",
        "http://127.0.0.1:5000/authentication/register",
        userData,
        handleSuccess,
        handleError
    );

}

function ajaxJoinRoom(roomId) {
    const userData = {
        room_id: roomId
    }

    makeAjaxRequest(
        "POST",
        "http://127.0.0.1:5000/chat/join_room",
        userData,
        handleSuccess,
        handleError
    );
}

function ajaxCreateRoom(roomName) {
    const userData = {
        room_name: roomName
    }

    makeAjaxRequest(
        "POST",
        "http://127.0.0.1:5000/chat/create_room",
        userData,
        handleSuccess,
        handleError
    );
}

function ajaxChangeUsername(newUsername, password) {
    const userData = {
        new_username: newUsername,
        password: password
    }

    makeAjaxRequest(
        "POST",
        "http://127.0.0.1:5000/edit_credentials/change_username",
        userData,
        handleSuccess,
        handleError
    );
}

function ajaxChangeEmail(newEmail, password) {
    const userData = {
        new_email: newEmail,
        password: password
    }

    makeAjaxRequest(
        "POST",
        "http://127.0.0.1:5000/edit_credentials/change_email",
        userData,
        handleSuccess,
        handleError
    );
}

function ajaxChangePassword(oldPassword, newPassword) {
    const userData = {
        old_password: oldPassword,
        new_password: newPassword
    }

    makeAjaxRequest(
        "POST",
        "http://127.0.0.1:5000/edit_credentials/change_password",
        userData,
        handleSuccess,
        handleError
    );
}

// Leave Room
function ajaxLeaveRoom(button) {
    const room_id = button.getAttribute("data-room-id");
    const username = button.getAttribute("data-username");
    const userData = {
        "room_id": room_id,
        "username": username
    };

    makeAjaxRequest(
        "POST",
        "http://127.0.0.1:5000/chat/leave_room",
        userData,
        handleSuccess,
        handleError
    );
}

// Change Room Name
function ajaxChangeRoomName(newRoomName, roomId) {
    const userData = {
        new_room_name: newRoomName,
        room_id: roomId
    }

    let baseUrl = "http://127.0.0.1:5000/chat/my_rooms/";
    makeAjaxRequest(
        "POST",
        `${baseUrl}${roomId}/edit`,
        userData,
        handleSuccess,
        handleError
    );
}

// Kick Member
function ajaxKickMember(button) {
    const room_id = button.getAttribute("data-room-id");
    const username = button.getAttribute("data-username");
    const userData = {
        "room_id": room_id,
        "username": username
    };

    makeAjaxRequest(
        "POST",
        "http://127.0.0.1:5000/chat/kick_member",
        userData,
        handleSuccess,
        handleError
    );
}