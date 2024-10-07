class Game {
	constructor(context, width, height) {
		this.context = context;
		this.width = width;
		this.height = height;
		this.ball = new Ball(width / 2, height / 2, 20, 10, 10);
		this.paddles = {
			left: new Paddle(0, height / 2 - 50, 20, 150, 15),
			right: new Paddle(width - 20, height / 2 - 50, 20, 150, 15)
		};
	}

	updateState(gameState) {
		// Sync with the game state received from the server
		if (gameState.ball)
			this.ball.updateState(gameState.ball);
		if (gameState.paddles) {
			this.paddles.left.updateState(gameState.paddles.left);
			this.paddles.right.updateState(gameState.paddles.right);
		}
	}

	render(){
		this.context.fillStyle = "rgba(0, 0, 0, 0.4)";
		this.context.fillRect(0, 0, this.width, this.height);
		this.ball.draw(this.context)
		this.paddles.left.draw(this.context)
		this.paddles.right.draw(this.context)
		drawGameFrame(this);
	}

	loop(keysPressed) {
		//this.update(keysPressed);
		this.render();
	}

}
