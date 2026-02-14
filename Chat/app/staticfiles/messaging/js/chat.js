// document.addEventListener("DOMContentLoaded", () => {
//     const messagesBox = document.getElementById("messages");
//     const form = document.getElementById("chat-form");
//     const recipientInput = document.getElementById("recipient-input");
//     const userStatus = document.getElementById("user-status");
//     const messageInput = document.getElementById("message-input");

//     if (!messagesBox || !form || !recipientInput) return;

//     let userExists = false;
//     let timeout = null;

//     console.log("Token:", ACCESS_TOKEN);
//     console.log("Host:", window.location.host);
    
//     const socket = new WebSocket(`ws://${window.location.host}/ws/chat/?token=${ACCESS_TOKEN}`);
    
//     socket.onopen = () => {
//         console.log("Conectado");
//     };
    
//     socket.onerror = (err) => {
//         console.log("Erro:", err);
//     };
    
//     socket.onclose = (e) => {
//         console.log("Fechado - Código:", e.code);
//     };

//     socket.onmessage = function (event) {
//         const data = JSON.parse(event.data);
//         const div = document.createElement("div");
//         div.className = "message";
//         div.innerHTML = `
//             <strong>De:</strong> ${data.sender}<br>
//             <p>${data.message}</p>
//             <small>${new Date().toLocaleString()}</small>
//         `;
//         messagesBox.prepend(div);
//     };

//     recipientInput.addEventListener("input", () => {
//         clearTimeout(timeout);
//         const username = recipientInput.value.trim();
//         userStatus.innerHTML = "";
//         userExists = false;

//         if (username.length < 3) return;

//         timeout = setTimeout(async () => {
//             try {
//                 const res = await fetch(
//                     `${API_BASE}/api/auth/check-username/?username=${username}`,
//                     { headers: { "Authorization": `Bearer ${ACCESS_TOKEN}` } }
//                 );
//                 const data = await res.json();
//                 userExists = data.exists;
//                 userStatus.innerHTML = data.exists ? "✅" : "❌";
//                 userStatus.style.color = data.exists ? "green" : "red";
//             } catch (err) {
//                 console.error(err);
//             }
//         }, 400);
//     });

//     async function loadMessages() {
//         try {
//             const res = await fetch(`${API_BASE}/api/auth/messages/`, {
//                 headers: { "Authorization": `Bearer ${ACCESS_TOKEN}` }
//             });
//             if (!res.ok) return;
//             const messages = await res.json();
//             messagesBox.innerHTML = "";
//             messages.forEach(msg => {
//                 const div = document.createElement("div");
//                 div.className = "message";
//                 div.innerHTML = `
//                     <strong>De:</strong> ${msg.sender}<br>
//                     <p>${msg.content}</p>
//                     <small>${new Date(msg.created_at).toLocaleString()}</small>
//                 `;
//                 messagesBox.appendChild(div);
//             });
//         } catch (err) {
//             console.error(err);
//         }
//     }

//     form.addEventListener("submit", e => {
//         e.preventDefault();
//         const username = recipientInput.value.trim();
//         const content = messageInput.value.trim();
//         if (!username || !content) return;
//         if (!userExists) {
//             alert("Usuário não existe");
//             return;
//         }
//         socket.send(JSON.stringify({
//             recipient: username,
//             content: content
//         }));
//         messageInput.value = "";
//     });

//     loadMessages();
// }); 