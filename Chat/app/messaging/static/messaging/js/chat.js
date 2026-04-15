document.addEventListener("DOMContentLoaded", () => {
    // UI Elements
    const contactListDiv = document.getElementById("contact-list");
    const messagesBox = document.getElementById("messages");
    const chatForm = document.getElementById("chat-form");
    const messageInput = document.getElementById("message-input");
    const searchInput = document.getElementById("new-contact-input");
    const searchStatus = document.getElementById("user-status-indicator");
    const chatAreaMain = document.getElementById("chat-area-main");
    const emptyStateView = document.getElementById("empty-state-view");
    const currentContactAvatar = document.getElementById("current-contact-avatar");
    const currentContactName = document.getElementById("current-contact-name");

    if (!messagesBox || !chatForm || !contactListDiv) return;

    // State Variables
    let allMessages = [];
    let currentContact = null;
    let searchTimeout = null;

    // Conectar Websocket
    const socket = new WebSocket(`ws://${window.location.host}/ws/chat/?token=${ACCESS_TOKEN}`);

    socket.onmessage = function (event) {
        const data = JSON.parse(event.data);
        if (data.error) return;

        // Formatar objeto padronizado para state
        const newMessage = {
            id: Date.now(),
            sender: data.sender,
            recipient: data.sender === CURRENT_USER ? currentContact : CURRENT_USER, 
            content: data.content || data.message,
            timestamp: new Date().toISOString()
        };

        allMessages.push(newMessage);
        
        // Se já tenho esse contato, atualiza. Se não for contato, vai criar ao renderizar
        renderContacts();

        // Se a mensagem for na conversa aberta, renderize
        if (currentContact === data.sender || (data.sender === CURRENT_USER)) {
            renderMessagesFor(currentContact);
        }
    };

    // Procurar por novo usuário
    searchInput.addEventListener("input", () => {
        clearTimeout(searchTimeout);
        const username = searchInput.value.trim();
        searchStatus.innerHTML = "";
        
        if (username.length < 3) return;
        if (username === CURRENT_USER) {
            searchStatus.innerHTML = "Você não pode conversar consigo mesmo.";
            searchStatus.style.color = "#8696a0";
            return;
        }

        searchTimeout = setTimeout(async () => {
            searchStatus.innerHTML = "Procurando usuario...";
            searchStatus.style.color = "#8696a0";
            try {
                const res = await fetch(`${API_BASE}/api/auth/check-username/?username=${username}`, {
                    headers: { Authorization: `Bearer ${ACCESS_TOKEN}` }
                });
                const data = await res.json();
                
                if (data.exists) {
                    searchStatus.innerHTML = `Usuário <strong>${username}</strong> encontrado! Abra-o clicando abaixo.`;
                    searchStatus.style.color = "#00a884";
                    // Forcar contato no topo
                    forceContactExistence(username);
                } else {
                    searchStatus.innerHTML = "Usuário não encontrado.";
                    searchStatus.style.color = "#ff4d4d";
                }
            } catch {
                searchStatus.innerHTML = "Erro ao buscar usuário.";
                searchStatus.style.color = "#ff4d4d";
            }
        }, 600);
    });

    function forceContactExistence(username) {
        // Se n temos mensagem com ele, cria um ficticio vazio pra forçar ele na UI
        const exist = allMessages.some(m => m.sender === username || m.recipient === username);
        if (!exist) {
            allMessages.push({
                placeholder: true,
                sender: CURRENT_USER,
                recipient: username,
                content: "",
                timestamp: new Date().toISOString()
            });
            renderContacts();
        }
    }

    // Processamento da API local
    async function fetchInitialMessages() {
        try {
            const res = await fetch(`${API_BASE}/api/auth/messages/`, {
                headers: { Authorization: `Bearer ${ACCESS_TOKEN}` }
            });
            if (!res.ok) return;
            const fetched = await res.json();
            allMessages = fetched.map(m => ({...m, placeholder: false}));
            renderContacts();
        } catch (e) {
            console.error("Failed to load messages", e);
        }
    }

    function renderContacts() {
        // Extrai contatos únicos
        const contactsMap = new Map();
        
        allMessages.forEach(msg => {
            const otherUser = msg.sender === CURRENT_USER ? msg.recipient : msg.sender;
            if (!otherUser) return;
            
            const time = new Date(msg.timestamp);
            
            // Só sobrescreve se essa msgs for mais nova que a guardada,
            // placeholders não atualizam ultima msg se já houver msg real.
            if (!contactsMap.has(otherUser)) {
                contactsMap.set(otherUser, { lastMessage: msg, time: time });
            } else {
                const existing = contactsMap.get(otherUser);
                if (time > existing.time && !msg.placeholder) {
                    contactsMap.set(otherUser, { lastMessage: msg, time: time });
                }
            }
        });

        // Converte pra Array e ordena do mais recente
        const sortedContacts = Array.from(contactsMap.entries())
            .sort((a, b) => b[1].time - a[1].time);

        contactListDiv.innerHTML = "";

        sortedContacts.forEach(([username, data]) => {
            const div = document.createElement("div");
            div.className = "contact-item";
            if (currentContact === username) {
                div.classList.add("active");
            }

            const initial = username.charAt(0).toUpperCase();
            
            let displayMsg = data.lastMessage.content;
            if (data.lastMessage.placeholder) displayMsg = "Nenhum histórico";
            else if (data.lastMessage.sender === CURRENT_USER) displayMsg = "Você: " + displayMsg;

            div.innerHTML = `
                <div class="avatar">${initial}</div>
                <div class="contact-info">
                    <div class="contact-name">${username}</div>
                    <div class="contact-last-msg">${displayMsg}</div>
                </div>
            `;

            div.onclick = () => openChat(username);
            contactListDiv.appendChild(div);
        });
    }

    function openChat(username) {
        currentContact = username;
        
        // Atualizar UI dos pains
        emptyStateView.style.display = "none";
        chatAreaMain.style.display = "flex";
        
        currentContactName.innerText = username;
        currentContactAvatar.innerText = username.charAt(0).toUpperCase();

        renderContacts(); // Atualizar css active state
        renderMessagesFor(username);
    }

    function renderMessagesFor(username) {
        messagesBox.innerHTML = "";
        
        const filtered = allMessages.filter(m => 
            !m.placeholder && (
            (m.sender === CURRENT_USER && m.recipient === username) ||
            (m.sender === username && m.recipient === CURRENT_USER)
            )
        );

        filtered.sort((a,b) => new Date(a.timestamp) - new Date(b.timestamp));

        filtered.forEach(msg => {
            const isMe = msg.sender === CURRENT_USER;
            const div = document.createElement("div");
            div.className = isMe ? "msg me" : "msg";
            
            const timeStr = new Date(msg.timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
            
            div.innerHTML = `
                <span>${msg.content}</span>
                <small>${timeStr}</small>
            `;
            messagesBox.appendChild(div);
        });
        
        messagesBox.scrollTop = messagesBox.scrollHeight;
    }

    // Submit do Chat
    chatForm.addEventListener("submit", e => {
        e.preventDefault();
        const content = messageInput.value.trim();
        if (!currentContact || !content) return;
        
        // WebSocket dispatch
        socket.send(JSON.stringify({ recipient: currentContact, content: content }));
        
        messageInput.value = "";
    });

    // Inicialização
    fetchInitialMessages();
});