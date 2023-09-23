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

    $('#join_room_modal_btn').click(function () {
        $('#join-room-modal-form').submit();
    });

    $('#create-room-modal-button').click(function () {
        $('#create-room-modal-form').submit();
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
            ajax_register_post(username, email, password)
        }
    });

    // Login Form
    $("#loginForm").submit(function (event) {
        event.preventDefault()
        if (validateLoginForm()) {
            let username = $("#username").val()
            let password = $("#password").val()
            ajax_login_post(username, password)
        }
    });

    // Join Room Modal Form
    $("#join-room-modal-form").submit(function (event) {
        event.preventDefault()
        if (validateJoinRoomModal()) {
            let room_id_input = $("#roomID").val()
            console.log(room_id_input)
            ajax_join_room_post(room_id_input)
        }
    });

    // Create Room Modal Form
    $("#create-room-modal-form").submit(function (event) {
        event.preventDefault()
        if (validateCreateRoomModal()) {
            let room_name_input = $("#roomName").val()
            ajax_create_room_post(room_name_input)
        }
    });

    // Change Username Modal Form
    $("#changeUsernameModalForm").submit(function (event) {
        event.preventDefault();
        if (validateChangeUsernameModalForm()) {
            let new_username = $("#newUsername").val()
            let password = $("#existingPassword1").val()
            ajax_change_username(new_username, password)
        }
    })

    // Change Email Modal Form
    $("#changeEmailModalForm").submit(function (event) {
        event.preventDefault();
        if (validateChangeEmailModalForm()) {
            let email = $("#newEmail").val()
            let password = $("#existingPassword2").val()
            ajax_change_email(email, password)
        }
    })

    // Change Password Modal Form
    $("#changePasswordModalForm").submit(function (event) {
        event.preventDefault();
        if (validateChangePasswordModalForm()) {
            let old_password = $("#oldPassword").val()
            let new_password = $("#newPassword").val()
            ajax_change_password(old_password, new_password)
        }
    })

    // Change Room Name Form
    $("#newRoomNameForm").submit(function (event) {
        event.preventDefault()
        if (validateNewRoomNameForm()) {
            let new_room_name = $("#new_room_name").val()
            let room_id = $("#room_id_div").text()
            ajax_change_room_name(new_room_name, room_id)
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

let customPopoutAlert = (message, status, alertDivId = "#alert") => {
    // Custom Alert Using Bootstrap
    let alertDiv = $(alertDivId)
    if (status === "success") {
        alertDiv.addClass("alert alert-success")
        alertDiv.text(message)
        setTimeout(function () {
            alertDiv.fadeOut("slow");
        }, 2000);
    } else {
        alertDiv.removeClass("fade out").addClass("alert alert-danger").show();
        alertDiv.text(message);

        setTimeout(function () {
            alertDiv.fadeOut("slow", function () {
                alertDiv.empty().removeClass(); // Clear the message and remove classes after fading out
            });
        }, 2000);
    }
}