let friends = [
];

let pendingRequests = [
];

async function populateFriendList(friend) {
    const friendList = document.getElementById('friendList');

    const existingFriend = friendList.querySelector(`.${friend.username}`);
    if (existingFriend) {
        return;
    }

    const friendElement = document.createElement('div');
    friendElement.className = 'chat-friend ' + friend.username;
    friendElement.id = friend.room_name;
    friendElement.innerHTML = `
        <a href="/profile?user=${friend.username}">
            <img src="${friend.photo}" alt="${friend.username}" class="chat-friend-avatar">
        </a>
        <div class="chat-friend-status ${friend.status}" id="status.${friend.username}"></div>
        <span class="chat-friend-name">${friend.username}</span>
        <button class="chat-friend-options-button" onclick="toggleOptions('${friend.username}-options')">:</button>
        <div class="chat-friend-options" id="${friend.username}-options" style="display: none;">
            <button class="chat-friend-block" id="${friend.blocked ? (friend.who_blocked + ' ' + friend.username) : ''}">
                ${friend.blocked ? 'Unblock' : 'Block'}
            </button>
                <button class="chat-friend-remove">Delete</button>
        </div>
    `;
    friendList.insertBefore(friendElement, friendList.lastElementChild);

    friendElement.querySelector('.chat-friend-block').addEventListener('click', function() {
        const buttonText = this.innerText;
        showPopup(`${friend.username} successfully ${buttonText.toLowerCase()}`, true);
        ws.send(JSON.stringify({
            'type': buttonText.includes('Unblock') ? 'unblock_friend' : 'block_friend',
            'name': friend.username
        }));
    });

    friendElement.querySelector('.chat-friend-remove').addEventListener('click', function() {
        friendElement.remove();
        showPopup(`Friend has been removed.`, true);
        ws.send(JSON.stringify({
            'type' : 'delete_friend',
            'name' : friend.username
        }));
    });
}

function toggleOptions(optionsId) {
    const optionsDiv = document.getElementById(optionsId);
    optionsDiv.style.display = optionsDiv.style.display === 'none' ? 'block' : 'none';
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
