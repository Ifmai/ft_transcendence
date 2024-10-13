async function pongPage() {
	const canvas = document.getElementById("pong");
	const context = canvas.getContext('2d');

	// Adjust the canvas size to fit the screen
	canvas.width = window.innerWidth;
	canvas.height = window.innerHeight;

	const room_id = getCodeURL('room');
	const wsUrl = `wss://lastdance.com.tr/ws-pong/pong/${room_id}/2/?token=${getCookie('access_token')}`;
	const socket = new WebSocket(wsUrl);


	const keysPressed = [];

	const keys = {
		38: "up",
		40: "down",
		87: "w",
		83: "s",
	};

	socket.onopen = function(event) {
		console.log('WebSocket connection opened:', event);
		socket.send(JSON.stringify({
			type: 'initialize',
			width: canvas.width,
			height: canvas.height
		}));
	};

	socket.onmessage = function(event) {
		const gameState = JSON.parse(event.data);
		console.log("game state: ", gameState);
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
			console.log(gameState['scores'])
			updateScoreDisplay(gameState['scores']);
		}
		if (gameState['won']){
			alert(gameState.won.message)
			socket.close();
			// if(!getCodeURL('tournament')){
			// 	loadPage(selectPage('/play'));
			// 	window.history.pushState({}, "", '/play');
			// }
		}
	};

	socket.onerror = function(error) {
		console.error('WebSocket error:', error);
	};

	socket.onclose = function(event) {
		console.log('WebSocket connection closed:', event);
	};


	window.addEventListener('keydown', function(event) {
		keysPressed[event.keyCode] = true;

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
};


//close eklencek
// soket init dışarı taşınabilir on message ile birlikte.
// url'i nasıl göndermemiz gerekiyor.
// direk pong-game mi olucak yoksa ekstra bilig gerekecek mi?