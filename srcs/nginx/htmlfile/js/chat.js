// // Friend list data
// const friends = [
//     { name: "Flynn", avatar: "/placeholder.svg?height=40&width=40" },
//     { name: "Quorra", avatar: "/placeholder.svg?height=40&width=40" },
//     { name: "Tron", avatar: "/placeholder.svg?height=40&width=40" },
//     { name: "Clu", avatar: "/placeholder.svg?height=40&width=40" },
//     { name: "Sam", avatar: "/placeholder.svg?height=40&width=40" }
// ];

// // Populate friend list
// const friendList = document.getElementById('friendList');
// friends.forEach(friend => {
//     const friendElement = document.createElement('div');
//     friendElement.className = 'chat-friend';
//     friendElement.innerHTML = `
//                 <img src="${friend.avatar}" alt="${friend.name}" class="chat-friend-avatar">
//                 <span class="chat-friend-name">${friend.name}</span>
//             `;
//     friendList.insertBefore(friendElement, friendList.lastElementChild);
// });

// // Chat functionality
// const chatMessages = document.getElementById('chatMessages');
// const messageInput = document.getElementById('messageInput');
// const sendButton = document.getElementById('sendButton');

// function addMessage(sender, content, avatar) {
//     const messageElement = document.createElement('div');
//     messageElement.className = 'chat-message';
//     messageElement.innerHTML = `
//                 <img src="${avatar}" alt="${sender}" class="chat-message-avatar">
//                 <div class="chat-message-content">
//                     <div class="chat-message-sender">${sender}</div>
//                     <div class="chat-message-text">${content}</div>
//                 </div>
//             `;
//     chatMessages.appendChild(messageElement);
//     chatMessages.scrollTop = chatMessages.scrollHeight;
// }

// sendButton.addEventListener('click', () => {
//     const message = messageInput.value.trim();
//     if (message) {
//         addMessage('You', message, '/placeholder.svg?height=40&width=40');
//         messageInput.value = '';
//     }
// });

// messageInput.addEventListener('keypress', (e) => {
//     if (e.key === 'Enter') {
//         sendButton.click();
//     }
// });

// // Add some initial messages
// addMessage('Flynn', 'Welcome to the TRONPONG chat!', '/placeholder.svg?height=40&width=40');
// addMessage('Quorra', 'Hey everyone! Ready for some intense matches?', '/placeholder.svg?height=40&width=40');
// addMessage('Tron', 'Remember, stay in the grid and watch out for those light cycles!', '/placeholder.svg?height=40&width=40');


let friendRequests = null;

function addFriendRequest(request) {
    const requestElement = document.createElement('div');
    requestElement.className = 'chat-friend-request';
    requestElement.innerHTML = `
                <img src="${request.avatar}" alt="${request.name}" class="chat-friend-request-avatar">
                <div class="chat-friend-request-info">
                    <div class="chat-friend-request-name">${request.name}</div>
                    <div class="chat-friend-request-actions">
                        <button class="chat-friend-request-accept">Accept</button>
                        <button class="chat-friend-request-reject">Reject</button>
                    </div>
                </div>
            `;
    friendRequests.appendChild(requestElement);
}

async function chatPage() {
    // Friend request functionality
    const friendRequestButton = document.getElementById('friendRequestButton');
    const friendRequestPopup = document.getElementById('friendRequestPopup');
    const overlay = document.getElementById('overlay');
    friendRequests = document.getElementById('friendRequests');
    const newFriendInput = document.getElementById('newFriendInput');
    const sendFriendRequestButton = document.getElementById('sendFriendRequestButton');
    
    friendRequestButton.addEventListener('click', () => {
        friendRequestPopup.style.display = 'block';
        overlay.style.display = 'block';
    });
    
    overlay.addEventListener('click', () => {
        friendRequestPopup.style.display = 'none';
        overlay.style.display = 'none';
    });
    
    // Sample friend request data
    const pendingRequests = [
        { name: "Rinzler", avatar: "/placeholder.svg?height=40&width=40" },
        { name: "Zuse", avatar: "/placeholder.svg?height=40&width=40" },
        { name: "Gem", avatar: "/placeholder.svg?height=40&width=40" }
    ];
    
    // Populate friend request list
    
    pendingRequests.forEach(addFriendRequest);
    
    // Handle friend request actions
    friendRequests.addEventListener('click', (e) => {
        if (e.target.classList.contains('chat-friend-request-accept') || e.target.classList.contains('chat-friend-request-reject')) {
            const requestElement = e.target.closest('.chat-friend-request');
            requestElement.remove();
        }
    });
    
    // Send new friend request
    sendFriendRequestButton.addEventListener('click', () => {
        const newFriendName = newFriendInput.value.trim();
        if (newFriendName) {
            addMessage('System', `Friend request sent to ${newFriendName}`, '/placeholder.svg?height=40&width=40');
            newFriendInput.value = '';
            friendRequestPopup.style.display = 'none';
            overlay.style.display = 'none';
        }
    });
    
    newFriendInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendFriendRequestButton.click();
        }
    });
}