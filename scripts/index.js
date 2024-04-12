function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

const id = getRandomInt(1, 100)
const socket = new WebSocket(`ws://127.0.0.1:8000/ws/${id}`) 
console.log(socket)

function showMessage(message) {
    const messageContainer = document.getElementById('container');
    const messageElement = document.createElement('div');
    messageElement.textContent = message;
    messageContainer.appendChild(messageElement);
}

// event listener for opening connection
socket.addEventListener('open', (event) => {
    showMessage('Connected to server.');
});

// event listener for receiving messages from the server
socket.onmessage = (event) => {
    showMessage(event.data)
}

// event listener for closing connection
socket.addEventListener('close', (event) => {
    showMessage('Connection closed.');
})

const inputText = document.getElementById('inputText');
const submitButton = document.getElementById('submitButton');

submitButton.addEventListener('click', function () {
    const inputValue = inputText.value;
    socket.send(inputValue)
});