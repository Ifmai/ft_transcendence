let ws_tournament;

async function tour_bracketPage() {
    tournamnet_id = getCodeURL('tournament');
	await initWebSocket_tournament();
    cleanupFunctions.push(closeWebSocket_tournament);
}

async function initWebSocket_tournament() {
    if (ws_tournament && ws_tournament.readyState === WebSocket.OPEN) {
        console.log('Turnuva soketi zaten açık');
        return;
    }else{
        token = getCookie('access_token')
        if(!token) {
            console.log('Kullanıcı oturum açmamış, WebSocket bağlantısı oluşturulmadı.');
            return;
        }
        else{
            ws_tournament = new WebSocket(`wss://10.11.22.5/ws-tournament/${getCodeURL('tournament')}/?token=${getCookie('access_token')}`);
            ws_tournament.onopen = function(event) {
                console.log('Torunament WebSocketi bağlantısı açıldı.');
                ws_tournament.send(JSON.stringify({
                    'type': 'init',
                    'message': 'Pending Tournament'
                }))
            };
        }
    }

    ws_tournament.onmessage = async function(event) {
        const data = JSON.parse(event.data);
        if(data['type'] == 'joined'){
            if(getPath() != `/pong-game`){
                player1 = document.getElementById('player1').querySelector('h3');
                player2 = document.getElementById('player2').querySelector('h3');
                player3 = document.getElementById('player3').querySelector('h3');
                player4 = document.getElementById('player4').querySelector('h3');
                if (data['message'][0]){
                    player1.innerText = data['message'][0];
                    document.getElementById('player1-status').classList.add('ready');
                }
                else if (!data['message'][0]) {
                    player1.innerText = 'Player 1';
                    document.getElementById('player1-status').classList.remove('ready');
                }
                if (data['message'][1]){
                    player2.innerText = data['message'][1];
                    document.getElementById('player2-status').classList.add('ready');
                }
                else if (!data['message'][1]){
                    player2.innerText = 'Player 2';
                    document.getElementById('player2-status').classList.remove('ready');
                }
                if (data['message'][2]){
                    player3.innerText = data['message'][2];
                    document.getElementById('player3-status').classList.add('ready');
                }
                else if (!data['message'][2]){
                    player3.innerText = 'Player 3';
                    document.getElementById('player3-status').classList.remove('ready');
                }
                if (data['message'][3]){
                    player4.innerText = data['message'][3];
                    document.getElementById('player4-status').classList.add('ready');
                }
                else if (!data['message'][3]){
                    player4.innerText = 'Player 4';
                    document.getElementById('player4-status').classList.remove('ready');
                }
            }
        }
        else if(data['type'] == 'winner_and_loser' || data['type'] == 'end_tournament')
        {
            if(data['winner'][0])
                document.getElementById('semifinal1').querySelector('h3').textContent = data['winner'][0];
            if(data['winner'][1])
                document.getElementById('semifinal2').querySelector('h3').textContent = data['winner'][1];
            if(data['winner'][2])
                document.getElementById('champion').querySelector('h3').textContent = data['winner'][2];
            if(data['type'] == 'winner_and_loser' && (!data['winner'][2])){
                await sleep(6000);
                ws_tournament.send(JSON.stringify({
                    'type': 'final_match_start',
                }))
            }
        }
        else if(data['type'] == 'end_tournament')
        {
            document.getElementById('champion').querySelector('h3').textContent = data['winner'];
        }
        else if(data['type'] == 'start')
        {
            ws_tournament.send(JSON.stringify({
                'type': 'start_match',
            }))
        }
        else if(data['type'] == 'match')
        {
            cleanupFunctions = [];
            window.history.pushState({}, "", `/pong-game?room=${data['match_id']}&match=${data['match_id']}&tournament=${getCodeURL('tournament')}`);
            await loadPage(selectPage('/pong-game'));
        }
    };

    ws_tournament.onclose = function(event) {
        console.log('WebSocket bağlantısı kapandı. Tournament Bracket Soketi.');
    };

    ws_tournament.onerror = function(event) {
        console.error('WebSocket hata:', event);
    };
}


function closeWebSocket_tournament() {
    if (ws_tournament) {
        ws_tournament.close();
        ws_tournament = null;
    }
}
