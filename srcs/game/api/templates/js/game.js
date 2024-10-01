class Game {
	constructor(context, width, height) {
		this.context = context;
		this.width = width;
		this.height = height;
		this.ball = { x: width / 2, y: height / 2, radius: 10, dx: 5, dy: 5 };
		this.paddles = {
			left: { x: 10, y: height / 2 - 50, width: 10, height: 100 },
			right: { x: width - 20, y: height / 2 - 50, width: 10, height: 100 }
		};
	}

	updateState(gameState) {
		// Sync with the game state received from the server
		this.ball = gameState.ball;
		this.paddles = gameState.paddles;
	}

	loop(keysPressed) {
		this.update(keysPressed);
		this.draw();
	}

	update(keysPressed) {
		// Paddle controls for multiplayer
		if (keysPressed[38]) this.paddles.right.y -= 10; // Up arrow
		if (keysPressed[40]) this.paddles.right.y += 10; // Down arrow
		if (keysPressed[87]) this.paddles.left.y -= 10;  // 'W' key
		if (keysPressed[83]) this.paddles.left.y += 10;  // 'S' key

		// Ball movement logic
		this.ball.x += this.ball.dx;
		this.ball.y += this.ball.dy;

		// Ball collision with walls
		if (this.ball.y + this.ball.radius > this.height || this.ball.y - this.ball.radius < 0) {
			this.ball.dy *= -1;
		}

		// Paddle collision detection (simplified)
		if (this.ball.x - this.ball.radius < this.paddles.left.x + this.paddles.left.width &&
			this.ball.y > this.paddles.left.y && this.ball.y < this.paddles.left.y + this.paddles.left.height) {
			this.ball.dx *= -1;
		}

		if (this.ball.x + this.ball.radius > this.paddles.right.x &&
			this.ball.y > this.paddles.right.y && this.ball.y < this.paddles.right.y + this.paddles.right.height) {
			this.ball.dx *= -1;
		}
	}

	draw() {
		// Clear the canvas
		this.context.clearRect(0, 0, this.width, this.height);

		// Draw paddles
		this.context.fillStyle = 'white';
		this.context.fillRect(this.paddles.left.x, this.paddles.left.y, this.paddles.left.width, this.paddles.left.height);
		this.context.fillRect(this.paddles.right.x, this.paddles.right.y, this.paddles.right.width, this.paddles.right.height);

		// Draw the ball
		this.context.beginPath();
		this.context.arc(this.ball.x, this.ball.y, this.ball.radius, 0, Math.PI * 2);
		this.context.fillStyle = 'white';
		this.context.fill();
		this.context.closePath();
	}
}
