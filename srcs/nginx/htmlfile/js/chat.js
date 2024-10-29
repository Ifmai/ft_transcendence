let now_chat_room;

async function get_chat_history() {
    chat_ws.send(JSON.stringify({
        'type': 'new_chat',
        'chat_room' : now_chat_room
    }));
}

function addMessage(sender, content, avatar) {
    const messageElement = document.createElement('div');
    messageElement.className = 'chat-message';
    messageElement.innerHTML = `
                <a href="/profile?user=${sender}">
                    <img src="${avatar}" alt="${sender}" class="chat-message-avatar">
                </a>
                <div class="chat-message-content">
                    <div class="chat-message-sender">${sender}</div>
                    <div class="chat-message-text">${content}</div>
                </div>
            `;
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function escapeHtml(unsafe) {
    return unsafe
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }


async function chatPage() {
    now_chat_room = 'global-chat';
    friendList();
    chat_ws_init();
    cleanupFunctions.push(closeWebSocket_chat);
    sendBtn = document.getElementById('sendButton');
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendBtn.click();
        }
    });
    sendBtn.addEventListener('click', async function () {
        const message = escapeHtml(messageInput.value.trim());
        if (message) {
            chat_ws.send(JSON.stringify({
                'type' : 'chat_message',
                'chat_room': now_chat_room,
                'message': message ,
            }));
            messageInput.value = '';
        }
    });
}

async function chat_ws_init() {
    if (chat_ws && chat_ws.readyState === WebSocket.OPEN) {
        console.log('Chat WebSocket zaten açık.');
        return;
    }

    chat_ws = new WebSocket(`wss://10.11.22.5/ws-chat/global-chat/?token=${getCookie('access_token')}`);
    chat_ws.onopen = function (event) {
        console.log('Chat WebSocket bağlantısı açıldı.');
    };

    chat_ws.onmessage = function (event) {
        const data = JSON.parse(event.data);
        if(data['type'] == 'chat'){
            if(data['chat_room'] == now_chat_room)
                addMessage(data['sender'], data['message'], data['photo']);
        }
        else if(data['type'] == 'history'){
            if(data['chat_room'] == now_chat_room)
                addMessage(data['sender'], data['message'], data['sender_photo']);
        }
    };

    chat_ws.onclose = function (event) {
        console.log('Chat WebSocket bağlantısı kapandı. Chat soketi.');
    };

    chat_ws.onerror = function (event) {
        console.error('Chat WebSocket hata:', event);
    };
}

function closeWebSocket_chat() {
    if (chat_ws) {
        chat_ws.close();
        chat_ws = null;
    }
}
