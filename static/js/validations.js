function initializeFormValidation(formId, rules, messages) {
    // custom email regex
    $.validator.methods.email = function (value, element) {
        return this.optional(element) || /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/.test(value);
    };

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

    return initializeFormValidation("#joinRoomModalForm", rules, messages);
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

    return initializeFormValidation("#createRoomModalForm", rules, messages);
}

function validateChangeUsernameModalForm() {
    const rules = {
        newUsername: {
            required: true
        },
        existingPassword1: {
            required: true
        }
    };

    const messages = {
        newUsername: {
            required: "New Username can't be blank!"
        },
        existingPassword1: {
            required: "Please input your password!"
        }
    };

    return initializeFormValidation("#changeUsernameModalForm", rules, messages)
}

function validateChangeEmailModalForm() {
    const rules = {
        newEmail: {
            required: true,
            email: true
        },
        existingPassword2: {
            required: true
        }
    };

    const messages = {
        newEmail: {
            required: "New Email can't be blank!",
            email: "Please provide a valid email address!"
        },
        existingPassword2: {
            required: "Please input your password!"
        }
    };

    return initializeFormValidation("#changeEmailModalForm", rules, messages)
}

function validateChangePasswordModalForm() {
    const rules = {
        oldPassword: {
            required: true
        },
        newPassword: {
            required: true
        },
        newPasswordConfirm: {
            required: true,
            equalTo: "#newPassword"
        }
    };

    const messages = {
        oldPassword: {
            required: "This field can't be blank!"
        },
        newPassword: {
            required: "This field can't be blank!"
        },
        newPasswordConfirm: {
            required: "This field can't be blank!",
            equalTo: "Passwords doesn't match!"
        }
    }

    return initializeFormValidation("#changePasswordModalForm", rules, messages)
}

function validateNewRoomNameForm() {
    const rules = {
        newRoomName: {
            required: true
        }
    }
    const messages = {
        newRoomName: {
            required: "New Room name can't be blank!"
        }
    }

    return initializeFormValidation("#newRoomNameForm", rules, messages)
}