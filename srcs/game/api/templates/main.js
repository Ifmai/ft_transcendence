async function fetchToken() {
    try {
        const response = await fetch('http://localhost:8000/api/get_test_token/');

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        if (!data.access_token) {
            throw new Error('Token not found in the response');
        }

        console.log('Token fetched successfully:', data.access_token);
        return data.access_token;
    } catch (error) {
        console.error('Error fetching token:', error);
        return null;
    }
}

window.onload = async function() {
	const canvas = document.getElementById("pong");
	const context = canvas.getContext('2d');

	// Adjust the canvas size to fit the screen
	canvas.width = window.innerWidth;
	canvas.height = window.innerHeight;


	fetchToken().then(token => {
		const wsUrl = `ws://localhost:8000/ws/pong/game_room_42/2/?token=${token}`;
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
			updateGameState(gameState);
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
	});
};
