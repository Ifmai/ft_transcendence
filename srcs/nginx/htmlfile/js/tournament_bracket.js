let ws_tournament;

const players = [
	{ id: 1, name: "Oyuncu 1", ready: false },
	{ id: 2, name: "Oyuncu 2", ready: false },
	{ id: 3, name: "Oyuncu 3", ready: false },
	{ id: 4, name: "Oyuncu 4", ready: false }
];

const winners = {
	semifinal1: null,
	semifinal2: null,
	final: null
};

let count_player = 0;

function startTournament() {
	winners.semifinal1 = Math.random() < 0.5 ? players[0] : players[1];
	winners.semifinal2 = Math.random() < 0.5 ? players[2] : players[3];

	document.getElementById('semifinal1').innerHTML = `<h3>${winners.semifinal1.name}</h3>`;
	document.getElementById('semifinal2').innerHTML = `<h3>${winners.semifinal2.name}</h3>`;

	setTimeout(() => {
		winners.final = Math.random() < 0.5 ? winners.semifinal1 : winners.semifinal2;
		document.getElementById('champion').innerHTML = `<h3>Şampiyon: ${winners.final.name}</h3>`;
	}, 2000);
}

async function tour_bracketPage() {
	//updatePlayerUI();
    tournamnet_id = getCodeURL('tournament');
	await initWebSocket_tournament();
    cleanupFunctions.push(() => closeWebSocket_tournament(tournamnet_id));
}

async function initWebSocket_tournament() {
    if (ws_tournament && ws_tournament.readyState === WebSocket.OPEN) {
        console.log('WebSocket zaten açık.');
        return;
    }
    token = getCookie('access_token')
    if(!token) {
        console.log('Kullanıcı oturum açmamış, WebSocket bağlantısı oluşturulmadı.');
        return;
    }

    // buraya bir if koncak eğer olmauan bir tournament id girilip sayfa erişimi sağlanmaya çalışılırsa home page yönlendir veya turnuvaya yönlendir.
    ws_tournament = new WebSocket(`wss://lastdance.com.tr/ws-tournament/${getCodeURL('tournament')}/?token=${getCookie('access_token')}`);
    ws_tournament.onopen = function(event) {
        console.log('WebSocket bağlantısı açıldı.');
        ws_tournament.send(JSON.stringify({
            'type': 'init',
            'message': 'Pending Tournament'
        }))
    };

    ws_tournament.onmessage = async function(event) {
        console.log("event data : ", event.data);
        const data = JSON.parse(event.data);
        console.log('gelend dataİ: ', data);
        if(data['type' == 'joined']){
            count_player += 1;
            //isimleri yerleştir.
        }
        else if(data['type'] == 'match'){
            loadPage(selectPage('/pong-game'));
            window.history.pushState({}, "", `/pong-game?room_id=${data['match_id']}&match=${data['match_id']}&tournament=${getCodeURL('tournament')}`);
        }

    };

    ws_tournament.onclose = function(event) {
        console.log('WebSocket bağlantısı kapandı. Tournament Bracket Soketi.');
    };

    ws_tournament.onerror = function(event) {
        console.error('WebSocket hata:', event);
    };
}

async function leave_tournament(tournamnet_id) {
    try {
		const response = await fetch('/api/tournament/', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'Authorization': `Bearer ${getCookie('access_token')}`
			},
			body: JSON.stringify({
                'tournament_id': tournamnet_id,
				'action' : 'leave'
            })
		});
		if(response.ok){
			const data = await response.json();
            console.log("gelen data : " , data);
		}
		else
			throw new Error(`HTTP error! Status: ${response.status}`);
	} catch (error) {
		console.error(error);
	}
}

function closeWebSocket_tournament(tournamnet_id) {
    if (ws_tournament) {
        console.log('tournament id : ', tournamnet_id);
        leave_tournament(tournamnet_id);
        ws_tournament.close();
        ws_tournament = null;
    }
}

// function checkAllReady() {
// 	if (players.every(player => player.ready)) {
// 		startTournament();
// 	}
// }

// function toggleReady(playerId) {
// 	const player = players.find(p => p.id === playerId);
// 	player.ready = !player.ready;
// 	updatePlayerUI(player);
// 	checkAllReady();
// }

// function updatePlayerUI(player) {
// 	const statusElement = document.getElementById(`player${player.id}-status`);
// 	const readyButton = document.getElementById(`player${player.id}-ready`);
// 	if (player.ready) {
// 		statusElement.classList.add('ready');
// 		readyButton.classList.add('active');
// 		readyButton.textContent = 'Hazır!';
// 	} else {
// 		statusElement.classList.remove('ready');
// 		readyButton.classList.remove('active');
// 		readyButton.textContent = 'Hazır';
// 	}
// }
