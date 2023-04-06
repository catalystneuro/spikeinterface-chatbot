const chatHistory = document.querySelector('#chat-history');
const form = document.querySelector('form');
const converter = new showdown.Converter();

form.addEventListener('submit', event => {
    event.preventDefault();
    const message = document.querySelector('input[name="message"]').value;
    chatHistory.innerHTML += `<div class="message user-message"><p><strong>Question:</strong> ${message}</p></div>`;

    fetch('/process_message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams(new FormData(form))
    })
        .then(response => response.json())
        .then(data => {
            const botHtmlResponse = converter.makeHtml(data.answer);
            chatHistory.innerHTML += `<div class="message bot-message"><p><strong>Answer:</strong></p>${botHtmlResponse}</div>`;

            const linksHtml = data.links.map(link => `<a href="${link}" target="_blank">${link}</a>`).join('<br>');
            chatHistory.innerHTML += `<div class="message bot-message"><p><strong>Relevant links in the documentation:</strong></p>${linksHtml}</div>`;

            form.reset();
            chatHistory.scrollTop = chatHistory.scrollHeight;
        });
});
