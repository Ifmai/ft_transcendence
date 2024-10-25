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
    player1 = document.getElementById('player1').querySelector('h3');
    player2 = document.getElementById('player2').querySelector('h3');
    player3 = document.getElementById('player3').querySelector('h3');
    player4 = document.getElementById('player4').querySelector('h3');
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
        if(data['type'] == 'joined'){
            //Burası Temize Çekilecek.
            if (data['message'][0]){
                player1.innerText = data['message'][0];
                document.getElementById('player1-status').classList.add('ready'); 
            }
            else if (!data['message'][0]) {
                player1.innerText = 'User 1';
                document.getElementById('player1-status').classList.remove('ready');
            }
            if (data['message'][1]){
                player2.innerText = data['message'][1];
                document.getElementById('player2-status').classList.add('ready'); 
            }
            else if (!data['message'][1]){
                player2.innerText = 'User 2';
                document.getElementById('player2-status').classList.remove('ready');
            }
            if (data['message'][2]){
                player3.innerText = data['message'][2];
                document.getElementById('player3-status').classList.add('ready'); 
            }
            else if (!data['message'][2]){
                player3.innerText = 'User 3';
                document.getElementById('player3-status').classList.remove('ready');
            }
            if (data['message'][3]){
                player4.innerText = data['message'][3];
                document.getElementById('player4-status').classList.add('ready'); 
            }
            else if (!data['message'][3]){
                player4.innerText = 'User 4';
                document.getElementById('player4-status').classList.remove('ready');
            }
        }
        else if(data['type'] == 'match'){
            cleanupFunctions = []
            loadPage(selectPage('/pong-game'));
            window.history.pushState({}, "", `/pong-game?room=${data['match_id']}&match=${data['match_id']}&tournament=${getCodeURL('tournament')}`);
        }
        else if(data['type'] == 'new_match'){
            ws_tournament.send(JSON.stringify({
                'type': 'final_match_start',
            }))
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