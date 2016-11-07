// Helper function for inserting HTML as the first child of an element.
function insert(targetId, message) {
    id(targetId).insertAdjacentHTML("beforeend", message);
}

// Helper function for selecting element by id.
function id(id) {
    return document.getElementById(id);
}

function htmlEscape(str) {
    return str
        .replace(/&/g, '&amp;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');
}

function htmlUnescape(str){
    return str
        .replace(/&quot;/g, '"')
        .replace(/&#39;/g, "'")
        .replace(/&lt;/g, '<')
        .replace(/&gt;/g, '>')
        .replace(/&amp;/g, '&');
}

// Update the chat-panel with a new entry.
function updateChatPanel(user, message) {
    var now = moment().format();
    insert("chat", "<p>" + now + ", " + user + ": " + htmlEscape(message) + "</p>");
}

// Update the chat-panel after a received message.
function updateChatReceive(msg) {
    updateChatPanel("ochu", msg.data);
}

// Send a message if it's not empty, then clear the input field.
function sendMessage(message) {
    if (message !== "") {
        updateChatPanel("you", message);
        socket.send(message);
        id("message").value = "";
    }
}

// Establish the WebSocket connection and set up event handlers.
var socket = new WebSocket("ws://" + window.location.host + "/chat/");

socket.onmessage = updateChatReceive;
socket.onclose = function () { alert("WebSocket connection closed") };

// Send message if "Send" is clicked.
id("send").addEventListener("click", function () {
    sendMessage(id("message").value);
});

// Send message if enter is pressed in the input field.
id("message").addEventListener("keypress", function (e) {
    if (e.keyCode === 13) { sendMessage(e.target.value); }
});
