async function initWebSocket_one_pvp_one() {
    if (ws_tournament && ws_tournament.readyState === WebSocket.OPEN) {
        console.log('WebSocket zaten açık.');
        return;
    }
    token = getCookie('access_token')
    if(!token) {
        console.log('Kullanıcı oturum açmamış, WebSocket bağlantısı oluşturulmadı.');
        return;
    }

    ws_tournament = new WebSocket(`wss://lastdance.com.tr/ws-match/matchmaking/2/?token=${getCookie('access_token')}`);
    ws_tournament.onopen = function(event) {
        console.log('1 vs 1 WebSocket bağlantısı açıldı.');
    };

    ws_tournament.onmessage = async function(event) {
        const data = JSON.parse(event.data);
        console.log('gelen room_id: ', data['room_id ']);
        if(data['room_id']){
            await closeWebSocket_one_pvp_one();
            window.history.pushState({}, "", `/pong-game?room=${data['room_id']}`);
            await loadPage(selectPage('/pong-game'));
        }
        if(data['message'] == 'No room found or player already in the queue'){
            await closeWebSocket_one_pvp_one();
            showPopup('Why 🤡? We know more than you', false, 5500);
            await sleep(1000);
            document.getElementById('matchPopup').style.display = 'none';
        }


    };

    ws_tournament.onclose = function(event) {
        console.log('WebSocket bağlantısı kapandı. 1 vs 1 Bracket Soketi.');
    };

    ws_tournament.onerror = function(event) {
        console.error('WebSocket hata:', event);
    };
}

async function closeWebSocket_one_pvp_one() {
    ws_tournament.close();
    ws_tournament = null;
}


async function playerPage() {
    how_to_play();
    document.getElementById('playNowLink').addEventListener('click', function(event) {
        event.preventDefault(); // Linkin varsayılan davranışını engelle
        initWebSocket_one_pvp_one();
        document.getElementById('matchPopup').style.display = 'flex';
    });

    document.getElementById('cancelBtn').addEventListener('click', async function() {
        await closeWebSocket_one_pvp_one();
        document.getElementById('matchPopup').style.display = 'none';
    });
}
