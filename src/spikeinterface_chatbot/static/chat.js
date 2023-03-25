const chatHistory = document.querySelector('#chat-history');
const form = document.querySelector('#chat-form');

form.addEventListener('submit', event => {
    event.preventDefault();

    const message = document.querySelector('input[name="message"]').value;
    chatHistory.innerHTML += `
        <div class="message user-message">
            <p><strong>Question:</strong> ${message}</p>
        </div>
    `;

    fetch('/process_message', { // Update this route to match your Flask route
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams(new FormData(form))
    })
    .then(response => response.text())
    .then(data => {
        chatHistory.innerHTML += `
            <div class="message bot-message">
                <p><strong>Answer:</strong> ${data}</p>
            </div>
        `;
        form.reset();
        chatHistory.scrollTop = chatHistory.scrollHeight;
    });
});
