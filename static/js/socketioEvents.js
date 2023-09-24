$(document).ready(function () {
    const username = $('#username_data').data('username');
    const room_id = $('#room_id_data').data('room_id');


    const socket = io.connect("http://127.0.0.1:5000") // socket connection
    // on connection
    socket.on("connect", function (data) {
        socket.emit('join_room', {
            username: username,
            room_id: room_id
        })
    })


    let message_input = document.getElementById("message_input")

    // message handling
    document.getElementById("message_input_form").onsubmit = function (e) {
        e.preventDefault(); // prevent form submitting by default
        let message = message_input.value.trim() // trim white spaces
        if (message.length) {
            // if the message length > 0
            socket.emit("send_message", {
                username: username,
                room_id: room_id,
                message: message
            })
        }
        message_input.value = "" // make the message input empty after sending a message
        message_input.focus()
    }

    window.onbeforeunload = function (data) {
        socket.emit('leave_room', {
            username: username,
            room_id: room_id
        })
    };

    // sent message, handling from python backend
    socket.on("receive_message", function (data) {
        const newNode = document.createElement("li")
        newNode.className = "d-flex"
        newNode.innerHTML = `<b>${data.username}:&nbsp;</b> ${data.message}`
        document.getElementById("messages_list").appendChild(newNode);
    })

    // join announcement handling
    socket.on("join_room_announcement", function (data) {
        const newNode = document.createElement("li")
        newNode.className = "d-flex"
        newNode.innerHTML = `<b>${data.username}&nbsp;</b>has joined the chat`
        document.getElementById("messages_list").appendChild(newNode);
    })

    // leave announcement handling
    socket.on('leave_room_announcement', function (data) {
        const newNode = document.createElement('li');
        newNode.className = "d-flex"
        newNode.innerHTML = `<b>${data.username}&nbsp;</b> has left the chat`;
        document.getElementById('messages_list').appendChild(newNode);
    });
})