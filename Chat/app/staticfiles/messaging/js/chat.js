document.addEventListener("DOMContentLoaded", () => {
    const messagesBox = document.getElementById("messages");
    const form = document.getElementById("chat-form");
    const recipientInput = document.getElementById("recipient-input");
    const userStatus = document.getElementById("user-status");
    const messageInput = document.getElementById("message-input");

    if (!messagesBox || !form || !recipientInput) return;

    let userExists = false;
    let timeout = null;

    const socket = new WebSocket(`ws://${window.location.host}/ws/chat/?token=${ACCESS_TOKEN}`);

    socket.onmessage = function (event) {
        const data = JSON.parse(event.data);
        if (data.error) return;

        const isMe = data.sender === CURRENT_USER;
        const div = document.createElement("div");
        div.className = isMe ? "msg me" : "msg";
        
        div.innerHTML = `
            <span>${data.content || data.message}</span>
            <small>${new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</small>
        `;

        messagesBox.appendChild(div);
        messagesBox.scrollTop = messagesBox.scrollHeight;
    };

    recipientInput.addEventListener("input", () => {
        clearTimeout(timeout);
        const username = recipientInput.value.trim();
        userStatus.innerHTML = "";
        userExists = false;
        if (username.length < 3) return;

        timeout = setTimeout(async () => {
            try {
                const res = await fetch(`${API_BASE}/api/auth/check-username/?username=${username}`, {
                    headers: { Authorization: `Bearer ${ACCESS_TOKEN}` }
                });
                const data = await res.json();
                userExists = data.exists;
                userStatus.innerHTML = data.exists ? "✅" : "❌";
                userStatus.style.color = data.exists ? "#4cc9f0" : "#f72585";
            } catch {
                userStatus.innerHTML = "❌";
            }
        }, 400);
    });

    async function loadMessages() {
        try {
            const res = await fetch(`${API_BASE}/api/auth/messages/`, {
                headers: { Authorization: `Bearer ${ACCESS_TOKEN}` }
            });
            if (!res.ok) return;
            const messages = await res.json();
            messagesBox.innerHTML = "";
            messages.forEach(msg => {
                const isMe = msg.sender === CURRENT_USER;
                const div = document.createElement("div");
                div.className = isMe ? "msg me" : "msg";
                div.innerHTML = `
                    <span>${msg.content}</span>
                    <small>${new Date(msg.created_at).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</small>
                `;
                messagesBox.appendChild(div);
            });
            messagesBox.scrollTop = messagesBox.scrollHeight;
        } catch {}
    }

    form.addEventListener("submit", e => {
        e.preventDefault();
        const username = recipientInput.value.trim();
        const content = messageInput.value.trim();
        if (!username || !content || !userExists) return;
        socket.send(JSON.stringify({ recipient: username, content: content }));
        messageInput.value = "";
    });

    loadMessages();
});