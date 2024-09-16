//friends js başlangıç.
async function add_friends(add_user) {
	try {
		const response = await fetch('https://lastdance.com.tr/api/users/addfriends/', {
			method: 'POST',
			headers:{
				'Content-Type': 'application/json',
				'Authorization': `Bearer ${getCookie('access_token')}`
			},
			body: JSON.stringify({
				username: add_user
			})
		});
		if(response.ok){
			window.history.pushState({}, "", "/chat");
			loadPage(selectPage());
		}
	} catch (error) {
		console.error(error);
	}
}

async function user_friends_list() {
	const response = await fetch('https://lastdance.com.tr/api/users/friends/', {
		method: 'GET',
		headers:{
			'Content-Type': 'application/json',
			'Authorization': `Bearer ${getCookie('access_token')}`
		}
	});
	const users = await response.json();
	const userList = document.getElementById('list-user');
	userList.innerHTML = '';
	users.forEach(user => {
		const li = document.createElement('li');
		li.textContent = user.friend_username;
		userList.appendChild(li);
	});
}

async function friends_accept(event) {
	if (event.target.tagName === 'BUTTON') {
		const button = event.target;
		const requestId = button.getAttribute('data-id');
		if (button.classList.contains('accept')) {
			const response = await fetch(`https://lastdance.com.tr/api/users/acceptfriends/${requestId}/`, {
				method: 'PUT',
				headers:{
					'Content-Type': 'application/json',
					'Authorization': `Bearer ${getCookie('access_token')}`
				},
				body: JSON.stringify({
					id: requestId
				})
			});
			if(response.ok){
				window.history.pushState({}, "", "/chat");
                loadPage(selectPage());
			}
		}
		else if (button.classList.contains('decline')) {
			const response = await fetch(`https://lastdance.com.tr/api/users/acceptfriends/${requestId}/`, {
				method: 'DELETE',
				headers:{
					'Content-Type': 'application/json',
					'Authorization': `Bearer ${getCookie('access_token')}`
				},
				body: JSON.stringify({
					id: requestId
				})
			});
			if(response.ok){
				window.history.pushState({}, "", "/chat");
                loadPage(selectPage());
			}
		}
	}
}


async function friends_request_list() {
	//friends_requests
	try {
		const response = await fetch('https://lastdance.com.tr/api/users/friends_requests/', {
			method: 'GET',
			headers:{
				'Content-Type': 'application/json',
				'Authorization': `Bearer ${getCookie('access_token')}`
			}
		});
		const requests = await response.json();
		const requestsList = document.getElementById('requests-list');
		requestsList.innerHTML = '';
		requests.forEach(request => {
            const li = document.createElement('li');
            li.innerHTML = `
                ${request.sender_username || 'Bilinmeyen Kullanıcı'}
                <button type="button" class="accept" data-id="${request.id}">Kabul Et</button>
                <button type="button" class="decline" data-id="${request.id}">Reddet</button>
            `;
            requestsList.appendChild(li);
        });
	} catch (error) {
		console.error(error);
	}
}
//Friends js bitiş.

//Chat başlangı.

async function initWebSocket2() {
    // WebSocket zaten açıksa, yeniden başlatma
    if (chat_ws && chat_ws.readyState === WebSocket.OPEN) {
        console.log('WebSocket zaten açık.');
        return;
    }

    // Yeni WebSocket bağlantısı oluştur
    chat_ws = new WebSocket(`wss://lastdance.com.tr/ws-chat/global-chat/?token=${getCookie('access_token')}`);
    chat_ws.onopen = function(event) {
        console.log('WebSocket bağlantısı açıldı.');
    };

    chat_ws.onmessage = function(event) {
        const data = JSON.parse(event.data);
        console.log('Gelen veri:', data);
    };

    chat_ws.onclose = function(event) {
        console.log('WebSocket bağlantısı kapandı.');
    };

    chat_ws.onerror = function(event) {
        console.error('WebSocket hata:', event);
    };
}

// WebSocket bağlantısını kapatma fonksiyonu
function closeWebSocket2() {
    if (chat_ws) {
        chat_ws.close();
        chat_ws = null;
    }
}

async function friendList() {
	initWebSocket2();
	const friendsBtn = document.getElementById('addFriends');
	const requestsList = document.getElementById('requests-list');

	await friends_request_list()
	await user_friends_list()
	friendsBtn.addEventListener('click', async function(event) {
		event.preventDefault();
		const usernameInput = document.getElementById('input-username').value;
		await add_friends(usernameInput);
	});
	requestsList.addEventListener('click', function(event) {
		event.preventDefault();
		friends_accept(event);
	});
}