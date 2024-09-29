function addMessage(sender, content, avatar) {
    const messageElement = document.createElement('div');
    messageElement.className = 'chat-message';
    messageElement.innerHTML = `
                <img src="${avatar}" alt="${sender}" class="chat-message-avatar">
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
    friendList();
    initWebSocket2();
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
                'message': message ,
            }));
            messageInput.value = '';
        }
    });
}

async function initWebSocket2() {
    if (chat_ws && chat_ws.readyState === WebSocket.OPEN) {
        console.log('WebSocket zaten açık.');
        return;
    }

    chat_ws = new WebSocket(`wss://lastdance.com.tr/ws-chat/global-chat/?token=${getCookie('access_token')}`);
    chat_ws.onopen = function (event) {
        console.log('WebSocket bağlantısı açıldı.');
    };

    chat_ws.onmessage = function (event) {
        const data = JSON.parse(event.data);
        if(data['type'] == 'chat')
            addMessage(data['sender'], data['message'], data['photo']);
    };

    chat_ws.onclose = function (event) {
        console.log('WebSocket bağlantısı kapandı.');
    };

    chat_ws.onerror = function (event) {
        console.error('WebSocket hata:', event);
    };
}

function closeWebSocket2() {
    if (chat_ws) {
        chat_ws.close();
        chat_ws = null;
    }
}