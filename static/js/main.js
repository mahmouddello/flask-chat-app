$(document).ready(function () {
    navbarActivating();

    // Add a click event listener to all navigation links
    const navLinks = document.querySelectorAll(".nav-link");
    navLinks.forEach(function (link) {
        link.addEventListener("click", function () {
            // Remove the "active" class from all navigation links
            navLinks.forEach(function (navLink) {
                navLink.classList.remove("active");
            });

            // Add the "active" class to the clicked link
            link.classList.add("active");
        });
    });

    // Monitor changes to the URL (e.g., back/forward navigation)
    window.addEventListener("popstate", navbarActivating);

    // button bindings

    $('#joinRoomModalBtn').click(function () {
        $('#joinRoomModalForm').submit();
    });

    $('#createRoomModalBtn').click(function () {
        $('#createRoomModalForm').submit();
    });

    $('#saveUsername').click(function () {
        $("#changeUsernameModalForm").submit();
    })

    $("#saveEmail").click(function () {
        $("#changeEmailModalForm").submit()
    })

    $("#savePassword").click(function () {
        $("#changePasswordModalForm").submit()
    })

    $("#saveRoomName").click(function () {
        $("#newRoomNameForm").submit()
    })

    // Register Form
    $("#registerForm").submit(function (event) {
        event.preventDefault();
        if (validateRegisterForm()) {
            let username, email, password;
            username = $("#username").val()
            email = $("#email").val()
            password = $("#password").val()
            ajaxRegister(username, email, password)
        }
    });

    // Login Form
    $("#loginForm").submit(function (event) {
        event.preventDefault()
        if (validateLoginForm()) {
            let username = $("#username").val()
            let password = $("#password").val()
            ajaxLogin(username, password)
        }
    });

    // Join Room Modal Form
    $("#joinRoomModalForm").submit(function (event) {
        event.preventDefault()
        if (validateJoinRoomModal()) {
            let roomIdInput = $("#roomID").val()
            ajaxJoinRoom(roomIdInput)
        }
    });

    // Create Room Modal Form
    $("#createRoomModalForm").submit(function (event) {
        event.preventDefault()
        if (validateCreateRoomModal()) {
            let roomNameInput = $("#roomName").val()
            ajaxCreateRoom(roomNameInput)
        }
    });

    // Change Username Modal Form
    $("#changeUsernameModalForm").submit(function (event) {
        event.preventDefault();
        if (validateChangeUsernameModalForm()) {
            let newUsername = $("#newUsername").val()
            let password = $("#existingPassword1").val()
            ajaxChangeUsername(newUsername, password)
        }
    })

    // Change Email Modal Form
    $("#changeEmailModalForm").submit(function (event) {
        event.preventDefault();
        if (validateChangeEmailModalForm()) {
            let email = $("#newEmail").val()
            let password = $("#existingPassword2").val()
            ajaxChangeEmail(email, password)
        }
    })

    // Change Password Modal Form
    $("#changePasswordModalForm").submit(function (event) {
        event.preventDefault();
        if (validateChangePasswordModalForm()) {
            let old_password = $("#oldPassword").val()
            let new_password = $("#newPassword").val()
            ajaxChangePassword(old_password, new_password)
        }
    })

    // Change Room Name Form
    $("#newRoomNameForm").submit(function (event) {
        event.preventDefault()
        if (validateNewRoomNameForm()) {
            let newRoomName = $("#newRoomName").val()
            let roomId = $("#roomIdDiv").text()
            ajaxChangeRoomName(newRoomName, roomId)
        }
    })

});

// Navbar Highlight Activating
let navbarActivating = () => {
    // Get the current URL path
    const currentPath = window.location.pathname;

    // Get all navigation links
    const navLinks = document.querySelectorAll(".nav-link");

    // Remove the "active" class from all navigation links
    navLinks.forEach(function (link) {
        link.classList.remove("active");
    });

    // Add the "active" class to the link corresponding to the current URL path
    navLinks.forEach(function (link) {
        const linkPath = link.getAttribute("href");
        if (linkPath === currentPath) {
            link.classList.add("active");
        }
    });
}

let customPopoutAlert = (message, status, alertDivId) => {
    // Custom Alert Using Bootstrap
    let alertDiv = $(alertDivId)
    if (status === "success") {
        alertDiv.addClass("alert alert-success")
        alertDiv.text(message)
        setTimeout(function () {
            alertDiv.fadeOut("slow");
        }, 1000);
    } else {
        alertDiv.removeClass("fade out").addClass("alert alert-danger").show();
        alertDiv.text(message);

        setTimeout(function () {
            alertDiv.fadeOut("slow", function () {
                alertDiv.empty().removeClass(); // Clear the message and remove classes after fading out
            });
        }, 1000);
    }
}