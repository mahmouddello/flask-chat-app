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
});

$(document).ready(function () {
    $("#registerForm").submit(function (event) {
        event.preventDefault();
        if (validateRegisterForm()) {
            let username, email, password;
            username = $("#username").val()
            email = $("#email").val()
            password = $("#password").val()
            console.log("NO REG VALIDATION PROBLEMS")
            ajax_register_post(username, email, password)
        }
    })
})

$(document).ready(function () {
    $("#loginForm").submit(function (event) {
        event.preventDefault()
        if (validateLoginForm()) {
            let username = $("#username").val()
            let password = $("#password").val()
            ajax_login_post(username, password)
        }
    })
});

$(document).ready(function () {
    $("#join-room-modal-form").submit(function (event) {
        event.preventDefault()
        if (validateJoinRoomModal()) {
            let room_id_input = $("#roomID").val()
            ajax_join_room_post(room_id_input)
        }
    })
})

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
                window.location.href = "http://127.0.0.1:5000/chat/my_rooms/"
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


// Login Validation
let validateLoginForm = () => {
    const $form = $("#loginForm");
    if ($form.length) {
        $form.validate({
            errorClass: "error", // Adding the error class to the error message element
            errorElement: "div", // Using div element to wrap the error message
            errorPlacement: function (error, element) {
                // Insert error message below the input field
                error.insertAfter(element);
            }, highlight: function (element) {
                // Adding "is-invalid" class to each invalid input field's parent div
                $(element).closest(".form-control").addClass("is-invalid");
            }, unhighlight: function (element) {
                // Remove "is-invalid" class from each correct input field's parent div
                $(element).closest(".form-control").removeClass("is-invalid");
            }, rules: {
                username: {
                    required: true
                }, password: {
                    required: true
                }
            }, messages: {
                username: {
                    required: "Username can't be empty"
                }, password: {
                    required: "Password can't be empty"
                }
            }
        })
        return $form.valid(); // true if form is validated
    }
    return false;
}

// Register Validation
let validateRegisterForm = () => {
    const $form = $("#registerForm");
    if ($form.length) {
        $form.validate({
            errorClass: "error", // Adding the error class to the error message element
            errorElement: "div", // Using div element to wrap the error message
            errorPlacement: function (error, element) {
                // Insert error message below each invalid input field
                error.insertAfter(element);
            },
            highlight: function (element) {
                // add "is-invalid" class to the input field's parent div
                $(element).closest(".form-control").addClass("is-invalid");
            },
            unhighlight: function (element) {
                // Remove "is-invalid" class from the input field's parent div
                $(element).closest(".form-control").removeClass("is-invalid");
            },
            rules: {
                username: {
                    required: true
                },
                email: {
                    required: true,
                },
                password: {
                    required: true,
                },
                password2: {
                    required: true,
                    equalTo: "#password"
                }
            },
            messages: {
                username: {
                    required: "Username is required"
                },
                email: {
                    required: "Email is required",
                },
                password: {
                    required: "Enter your password"
                },
                password2: {
                    required: "Confirm your password",
                    equalTo: "Passwords doesn't match"
                }
            },
        });
        return $form.valid(); // true if form is validated
    }
    return false;
}

let validateJoinRoomModal = () => {
    const $modal_form = $("#join-room-modal-form")
    if ($modal_form.length) {
        $modal_form.validate({
            errorClass: "error", // Adding the error class to the error message element
            errorElement: "div", // Using div element to wrap the error message
            errorPlacement: function (error, element) {
                // Insert error message below each invalid input field
                error.insertAfter(element);
            },
            highlight: function (element) {
                // add "is-invalid" class to the input field's parent div
                $(element).closest(".form-control").addClass("is-invalid");
            },
            unhighlight: function (element) {
                // Remove "is-invalid" class from the input field's parent div
                $(element).closest(".form-control").removeClass("is-invalid");
            },
            rules: {
                roomID: {
                    required: true
                }
            },
            messages: {
                roomID: {
                    required: "Room ID field can't be blank!"
                }
            },
        });
        return $modal_form.valid(); // true if form is validated
    }
    return false;
}

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

let customPopoutAlert = (message, status) => {
    // Custom Alert Using Bootstrap
    let alertDiv = $("#alert")
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