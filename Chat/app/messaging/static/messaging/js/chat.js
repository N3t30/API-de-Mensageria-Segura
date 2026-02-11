document.addEventListener("DOMContentLoaded", () => {

    const messagesBox = document.getElementById("messages");
    const form = document.getElementById("chat-form");
    const recipientInput = document.getElementById("recipient-input");
    const userStatus = document.getElementById("user-status");

    if (!messagesBox || !form || !recipientInput) return;

    let userExists = false;
    let timeout = null;

    recipientInput.addEventListener("input", () => {
        clearTimeout(timeout);

        const username = recipientInput.value.trim();
        userStatus.innerHTML = "";
        userExists = false;

        if (username.length < 3) return;

        timeout = setTimeout(async () => {
            try {
                const res = await fetch(
                    `${API_BASE}/api/auth/check-username/?username=${username}`,
                    {
                        headers: {
                            "Authorization": `Bearer ${ACCESS_TOKEN}`
                        }
                    }
                );

                const data = await res.json();

                if (data.exists) {
                    userStatus.innerHTML = "✅";
                    userStatus.style.color = "green";
                    userExists = true;
                } else {
                    userStatus.innerHTML = "❌";
                    userStatus.style.color = "red";
                }
            } catch (err) {
                console.error(err);
            }
        }, 400);
    });

    async function loadMessages() {
        try {
            const res = await fetch(`${API_BASE}/api/auth/messages/`, {
                headers: {
                    "Authorization": `Bearer ${ACCESS_TOKEN}`
                }
            });

            if (!res.ok) return;

            const messages = await res.json();
            messagesBox.innerHTML = "";

            messages.forEach(msg => {
                const div = document.createElement("div");
                div.className = "message";
                div.innerHTML = `
                    <strong>De:</strong> ${msg.sender}<br>
                    <p>${msg.content}</p>
                    <small>${new Date(msg.created_at).toLocaleString()}</small>
                `;
                messagesBox.appendChild(div);
            });
        } catch (err) {
            console.error(err);
        }
    }

    form.addEventListener("submit", async e => {
        e.preventDefault();

        const username = recipientInput.value.trim();
        const content = document.getElementById("message-input").value.trim();

        if (!username || !content) return;

        if (!userExists) {
            alert("Usuário não existe");
            return;
        }

        try {
            const res = await fetch(`${API_BASE}/api/auth/send/`, {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${ACCESS_TOKEN}`,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    username: username,
                    content: content,
                    ttl_seconds: 300
                })
            });

            if (!res.ok) {
                alert("Erro ao enviar mensagem");
                return;
            }

            recipientInput.value = "";
            document.getElementById("message-input").value = "";
            userStatus.innerHTML = "";
            userExists = false;

            loadMessages();
        } catch (err) {
            console.error(err);
        }
    });

    loadMessages();
});
