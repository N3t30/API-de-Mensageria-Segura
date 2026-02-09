const usersContainer = document.querySelector(".users");
const chatPanel = document.getElementById("chat");
const chatHeader = document.getElementById("chat-header");
const messagesBox = document.getElementById("messages");

let selectedUserId = null;

async function loadUsers() {
    const res = await fetch(`${API_BASE}/api/auth/users/`, {
        headers: {
            "Authorization": `Bearer ${ACCESS_TOKEN}`
        }
    });

    const users = await res.json();

    usersContainer.innerHTML = "<h3>Usuários</h3>";

    users.forEach(user => {
        const div = document.createElement("div");
        div.className = "user";
        div.textContent = user.username;
        div.onclick = () => openChat(user);
        usersContainer.appendChild(div);
    });
}

function openChat(user) {
    selectedUserId = user.id;
    chatHeader.textContent = user.username;
    chatPanel.classList.remove("hidden");
    messagesBox.innerHTML = "";
}

document.getElementById("chat-form").addEventListener("submit", async e => {
    e.preventDefault();

    const input = document.getElementById("message-input");
    const content = input.value.trim();
    if (!content || !selectedUserId) return;

    await fetch(`${API_BASE}/api/auth/messages/`, {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${ACCESS_TOKEN}`,
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            recipient: selectedUserId,
            content: content,
            ttl_seconds: 300
        })
    });

    input.value = "";
});

loadUsers();
