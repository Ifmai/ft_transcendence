class Game {
	constructor(context, width, height, mode) {
		this.context = context;
		this.width = width;
		this.height = height;
		this.mode = mode;
		this.ball = new Ball(vec2(200, 200), vec2(8, 8), 20);
		this.paddle1 = new Paddle(vec2(0, 50), vec2(10, 10), 20, 160);
		this.paddle2 = new Paddle(vec2(width-20, 200), vec2(10, 10), 20, 160);
	}


	update(keysPressed) {
		this.ball.update();
		this.paddle1.update(keysPressed, 1);
		if (this.mode === "ai") {
			AIPlayer(this);
		} else if (this.mode === "multiplayer") {
			this.paddle2.update(keysPressed, 2);
		}
		ballCollisionWithTheEdges(this);
		paddleCollisionWithTheEdges(this);
		ballCollisionWithThePaddle(this);
		gameScore(this);
	}

	render(isPaused) {
		this.context.fillStyle = "rgba(0, 0, 0, 0.4)";
		this.context.fillRect(0, 0, this.width, this.height);
		this.ball.draw(this.context);
		this.paddle1.draw(this.context);
		this.paddle2.draw(this.context);
		drawGameFrame(this);

		if (isPaused)
			pauseTable(this);
	}

	loop(keysPressed, isPaused) {
		if (!isPaused) {
			this.update(keysPressed);
		}
		this.render(isPaused);
	}
}
