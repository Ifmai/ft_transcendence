let friends = [
];

let pendingRequests = [
];

async function populateFriendList(friend) {
    const friendList = document.getElementById('friendList');

    const existingFriend = friendList.querySelector(`#${friend.username}`);
    if (existingFriend) {
        return;
    }

    const friendElement = document.createElement('div');
    friendElement.className = 'chat-friend';
    friendElement.id = friend.room_name;
    friendElement.innerHTML = `
            <img src="${friend.photo}" alt="${friend.username}" class="chat-friend-avatar">
            <span class="chat-friend-name">${friend.username}</span>
            <div class="chat-friend-status ${friend.status}" id="status.${friend.username}"></div>
        `;
    friendList.insertBefore(friendElement, friendList.lastElementChild);
}

function addFriendRequest(request) {
    const friendRequests = document.getElementById('friendRequests');

    const existingFriend = friendRequests.querySelector(`#${request.username}`);
    if (existingFriend) {
        return;
    }

    const requestElement = document.createElement('div');
    requestElement.className = 'chat-friend-request';
    requestElement.innerHTML = `
                <img src="${request.photo}" alt="${request.username}" class="chat-friend-request-avatar">
                <div class="chat-friend-request-info">
                    <div class="chat-friend-request-name">${request.username}</div>
                    <div class="chat-friend-request-actions">
                        <button class="chat-friend-request-accept" id="${request.username}">Accept</button>
                        <button class="chat-friend-request-reject" id="${request.username}">Reject</button>
                    </div>
                </div>
            `;
    friendRequests.appendChild(requestElement);
}

async function sendListRequest() {
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ 
            'type': 'list_request',
        }));
    } else {
        console.log('Waiting connection...');
        setTimeout(sendListRequest, 1000);
    }
}

async function friendList() {
    const friendRequests = document.getElementById('friendRequests');
    const sendFriendRequestButton = document.getElementById('sendFriendRequestButton');
    const friendRequestButton = document.getElementById('friendRequestButton');
    const friendRequestPopup = document.getElementById('friendRequestPopup');
    const newFriendInput = document.getElementById('newFriendInput');
    const overlay = document.getElementById('overlay');
    const container = document.getElementById('friendList');

    sendListRequest();
    container.addEventListener('click', (e) => {
        if (e.target.classList.contains('chat-friend')) {
            const chat_box = document.getElementById('chatMessages');
            chat_box.innerHTML = '';
            now_chat_room = e.target.id;
            if(e.target.id != 'global-chat')
                get_chat_history(e.target.id);
        }
    });

    friendRequests.addEventListener('click', (e) => {
        if (e.target.classList.contains('chat-friend-request-accept') || e.target.classList.contains('chat-friend-request-reject')) {
            const friendId = e.target.id;
            let response;
            if(e.target.classList.contains('chat-friend-request-accept'))
                response = 'accept';
            else
                response = 'reject';
            ws.send(JSON.stringify({
                'type' : 'friend_request_response',
                'username': friendId,
                'response' : response
            }));
            const requestElement = e.target.closest('.chat-friend-request');
            requestElement.remove();
        }
    });

    newFriendInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendFriendRequestButton.click();
        }
    });

    sendFriendRequestButton.addEventListener('click', () => {
        const newFriendName = newFriendInput.value.trim();
        if (newFriendName) {
            addMessage('System', `Friend request sent to ${newFriendName}`, '/placeholder.svg?height=40&width=40');
            ws.send(JSON.stringify({
                'type': 'friend_request',
                'name': newFriendName
            }));
            newFriendInput.value = '';
        }
    });

    friendRequestButton.addEventListener('click', () => {
        friendRequestPopup.style.display = 'block';
        overlay.style.display = 'block';
        ws.send(JSON.stringify({
            'type' : 'friend_request_list'
        }));
    });
    overlay.addEventListener('click', () => {
        friendRequestPopup.style.display = 'none';
        overlay.style.display = 'none';
    });
}


async function initWebSocket() {
    if (ws && ws.readyState === WebSocket.OPEN) {
        console.log('WebSocket zaten açık.');
        return;
    }
    token = getCookie('access_token')
    if(!token) {
        console.log('Kullanıcı oturum açmamış, WebSocket bağlantısı oluşturulmadı.');
        return;
    }

    // Yeni WebSocket bağlantısı oluştur
    ws = new WebSocket(`wss://lastdance.com.tr/ws/friend-list/?token=${getCookie('access_token')}`);
    ws.onopen = function(event) {
        console.log('WebSocket bağlantısı açıldı.');
    };

    ws.onmessage = async function(event) {
        const data = JSON.parse(event.data);
        if(data['type'] == 'activity'){
            friends = []
            const friend = {
                'username': data['user'],
                'photo': data['photo'],
                'status': data['status'],
                'room_name': data['room_name']
            }
            friends.push(friend);
            populateFriendList(friend);
        }
        else if (data['type'] == 'friend_status'){
            const statusDiv = document.getElementById('status.' + data['username']);
            const newStatus = data['status']
            console.log("Status div : ", statusDiv);
            if (statusDiv) {
                statusDiv.className = newStatus === 'ON' ? 'chat-friend-status ON' : 'chat-friend-status OF';
            }
        }
        else if(data['type'] == 'request_list'){
            pendingRequests = []
            const friend = {
                'username': data['user'],
                'photo': data['photo']
            }
            pendingRequests.push(friend);
            addFriendRequest(friend);
        }
        else if(data['type'] == 'friend_request_response'){
            if(data['Response'] == 'accepted'){
                ws.send(JSON.stringify({ 
                    'type' : 'list_request',
                }));
            }
            ws.send(JSON.stringify({ 
                'type' : 'friend_request_list',
            }));
        }
    };

    ws.onclose = function(event) {
        console.log('WebSocket bağlantısı kapandı.');
    };

    ws.onerror = function(event) {
        console.error('WebSocket hata:', event);
    };
}

//WebSocket bağlantısını kapatma fonksiyonu
function closeWebSocket() {
    if (ws) {
        ws.close();
        ws = null;
    }
}