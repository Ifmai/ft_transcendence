let right_player_name;
let left_player_name;

async function pongPage() {
	const canvas = document.getElementById("pong");
	const context = canvas.getContext('2d');


	// Adjust the canvas size to fit the screen
	canvas.width = 1200;
	canvas.height = 800;

	const room_id = getCodeURL('room');
	const match_id = getCodeURL('match');
	const tournament = getCodeURL('tournament');


	let wsUrl;

	if(match_id){
		wsUrl = `wss://10.11.22.5/ws-pong/pong/${room_id}/${match_id}/?token=${getCookie('access_token')}`;
	}
	else{
		wsUrl = `wss://10.11.22.5/ws-pong/pong/${room_id}/?token=${getCookie('access_token')}`;
	}
	const socket = new WebSocket(wsUrl);
	if(tournament)
		initWebSocket_tournament();
	const keysPressed = [];

	const keys = {
		38: "up",
		40: "down",
		87: "w",
		83: "s",
		32 : "space",
	};

	socket.onopen = function(event) {
		console.log('WebSocket connection opened:', event);
		socket.send(JSON.stringify({ type: 'initialize' }));
	};

	function sleep(ms) {
		return new Promise(resolve => setTimeout(resolve, ms));
	}

	socket.onmessage = async function(event) {
		const gameState = JSON.parse(event.data);
		if (gameState['type'] == 'initialize')
		{
			updateGameState(gameState);
		}
		if (gameState['paddles']) {
			Object.keys(gameState.paddles).forEach((paddle) => {
				game.paddles[paddle].updateState(gameState.paddles[paddle]);
			});
		}
		if (gameState['ball']) {
			game.ball.updateState(gameState.ball)
		}
		if (gameState['scores']) {
			updateScoreDisplay(gameState['scores']);
		}
		if (gameState['end']){
			if(!tournament){
				await sleep(2000);
				socket.close();
				await loadPage(selectPage('/play'));
				window.history.pushState({}, "", '/play');
			}
			else if(tournament){
				await sleep(1500);
				socket.close();
				window.history.pushState({}, "", `/tournament?tournament=${tournament}`);
				await loadPage(selectPage('/tournament'));
			}
		}
		if (gameState['won']){
			if (ws_tournament && ws_tournament.readyState === WebSocket.OPEN){
				ws_tournament.send(JSON.stringify({
					'type' : 'won_user',
					'winner_name': gameState['won'],
					'loser_name': gameState['lost']
				}));
			}
		}
		if (gameState['PowerUp'])
		{
			const side = gameState['PowerUp'];
			if (side === 'left') {
				game.paddles.left.neon = 1;
			}
			else if (side === 'right') {
				game.paddles.right.neon = 1;
			}
			await sleep(5000)
				if (side == 'left'){
					game.paddles.left.neon = 0}
				else if (side == 'right'){
					game.paddles.right.neon = 0;
				}


		}
		if (gameState['type'] == 'initialize'){
			if(gameState['message'] == 'len 1'){
				socket.send(JSON.stringify({
					type: 'initialize',
				}));
			}
			else if(gameState['message'] == 'len 2'){
				left_player_name = gameState['left'];
				right_player_name = gameState['right'];

				// Oyuncu isimlerini göster
				const leftPlayerNameElement = document.getElementById('leftPlayerName');
				const rightPlayerNameElement = document.getElementById('rightPlayerName');
				const playerNamesElement = document.getElementById('playerNames');

				leftPlayerNameElement.textContent = left_player_name;
				rightPlayerNameElement.textContent = right_player_name;
				playerNamesElement.style.opacity = '1';

				// Canvas'a blur efekti ekle
				canvas.classList.add('blur');

				// 5 saniye bekle ve efektleri kaldır
					await sleep(4500);
					playerNamesElement.style.opacity = '0';
					canvas.classList.remove('blur');

					// Biraz daha bekle ve oyunu başlat
					await sleep(500);
					socket.send(JSON.stringify({
						type: 'start',
						width: canvas.width,
						height: canvas.height,
					}));

			}
		}
	};

	socket.onerror = function(error) {
		console.error('WebSocket error:', error);
	};

	socket.onclose = function(event) {
		console.log('WebSocket connection closed:', event);
		sessionStorage.setItem("isRefreshing", "false");
		sessionStorage.removeItem("isRefreshing");

	};

	window.addEventListener('keydown', function(event) {
		keysPressed[event.keyCode] = true;
		if (event.key === "ArrowDown" || event.key === "ArrowUp" || event.keyCode === 32){
			event.preventDefault();
		}
		if (socket && socket.readyState === WebSocket.OPEN && event.keyCode in keys) {
			socket.send(JSON.stringify({ type: "keyPress", keyCode: event.keyCode, state: "down" }));
		}
	});

	window.addEventListener('keyup', function(event) {
		keysPressed[event.keyCode] = false;
		if (socket && socket.readyState === WebSocket.OPEN && event.keyCode in keys) {
			socket.send(JSON.stringify({ type: "keyPress", keyCode: event.keyCode, state: "up" }));
		}
	});

	// Initialize the Pong game
	const game = new Game(context, canvas.width, canvas.height);

	function gameLoop() {
		game.loop(keysPressed);
		requestAnimationFrame(gameLoop);
	}

	gameLoop();


	function updateGameState(gameState) {
		// Update game logic based on server-side game state
		game.updateState(gameState);
	}
}
