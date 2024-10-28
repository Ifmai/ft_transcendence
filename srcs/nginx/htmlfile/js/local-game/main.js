window.onload = function() {
	const canvas = document.getElementById("pong");
	const context = canvas.getContext('2d');
	const menu = document.getElementById("menu");

	canvas.width = window.innerWidth;
	canvas.height = window.innerHeight;
	canvas.style.display = 'none';

	const keysPressed = [];
	let isPaused = false;

	document.getElementById("aiMode").addEventListener("click", function() {
		initGame("ai");
	});

	document.getElementById("multiplayerMode").addEventListener("click", function() {
		initGame("multiplayer");
	});

	window.addEventListener('keydown', function(event)
	{
		keysPressed[event.keyCode] = true;

		if (event.keyCode === PAUSE)
		{
			isPaused = !isPaused;
		}
	});

	window.addEventListener('keyup', function(event)
	{
		keysPressed[event.keyCode] = false;
	});


	function initGame(mode) {
		menu.style.display = 'none';
		canvas.style.display = 'block';
		const game = new Game(context, canvas.width, canvas.height, mode);

		function gameLoop() {
			game.loop(keysPressed, isPaused);
			requestAnimationFrame(gameLoop);
		}

		gameLoop();
	}
};
