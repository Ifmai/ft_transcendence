class Game {
	constructor(context, width, height) {
		this.context = context;
		this.width = width;
		this.height = height;
		this.ball = new Ball(width / 2, height / 2, 20, 10, 10);
		this.paddles = {
			left: { x: 10, y: height / 2 - 50, width: 10, height: 100 },
			right: { x: width - 20, y: height / 2 - 50, width: 10, height: 100 }
		};
	}

	updateState(gameState) {
		// Sync with the game state received from the server
		if (gameState.ball)
			this.ball.updateState(gameState.ball);
		this.paddles = gameState.paddles;
	}

	render(){
		this.context.fillStyle = "rgba(0, 0, 0, 0.4)";
		this.context.fillRect(0, 0, this.width, this.height);
		this.ball.draw(this.context)
		drawGameFrame(this);
	}

	loop(keysPressed) {
		//this.update(keysPressed);
		this.render();
	}

}
