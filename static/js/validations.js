function initializeFormValidation(formId, rules, messages) {
    const $form = $(formId);
    if ($form.length) {
        $form.validate({
            errorClass: "error",
            errorElement: "div",
            errorPlacement: function (error, element) {
                error.insertAfter(element);
            },
            highlight: function (element) {
                $(element).closest(".form-control").addClass("is-invalid");
            },
            unhighlight: function (element) {
                $(element).closest(".form-control").removeClass("is-invalid");
            },
            rules: rules,
            messages: messages,
        });
        return $form.valid();
    }
    return false;
}

// Login Validation
function validateLoginForm() {
    const rules = {
        username: {
            required: true
        },
        password: {
            required: true
        }
    };

    const messages = {
        username: {
            required: "Username can't be empty"
        },
        password: {
            required: "Password can't be empty"
        }
    };

    return initializeFormValidation("#loginForm", rules, messages);
}

// Register Validation
function validateRegisterForm() {
    const rules = {
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
    };

    const messages = {
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
            equalTo: "Passwords don't match"
        }
    };

    return initializeFormValidation("#registerForm", rules, messages);
}

// Join Room Modal Validation
function validateJoinRoomModal() {
    const rules = {
        roomID: {
            required: true
        }
    };

    const messages = {
        roomID: {
            required: "Room ID field can't be blank!"
        }
    };

    return initializeFormValidation("#join-room-modal-form", rules, messages);
}

// Create Room Modal Validation
function validateCreateRoomModal() {
    const rules = {
        roomName: {
            required: true
        }
    };

    const messages = {
        roomName: {
            required: "Room Name field can't be blank!"
        }
    };

    return initializeFormValidation("#create-room-modal-form", rules, messages);
}