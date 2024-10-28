// Utility function for creating 2D vectors
function vec2(x, y) {
	return { x, y };
}

function ballCollisionWithTheEdges(game) {
	if (game.ball.pos.y + game.ball.radius > game.height || game.ball.pos.y - game.ball.radius <= 0) {
		game.ball.velocity.y *= -1;
	}
}

function paddleCollisionWithTheEdges(game) {
	if (game.paddle1.pos.y <= 0)
		game.paddle1.pos.y = 0;

	if (game.paddle1.pos.y + game.paddle1.height >= game.height)
			game.paddle1.pos.y = game.height - game.paddle1.height;

	if (game.paddle2.pos.y <= 0)
		game.paddle2.pos.y = 0;

	if (game.paddle2.pos.y + game.paddle2.height >= game.height)
			game.paddle2.pos.y = game.height - game.paddle2.height;
}


function ballCollisionWithThePaddle(game) {
	let dx1 =  Math.abs(game.ball.pos.x - game.paddle1.getCenter().x);
	let dy1 =  Math.abs(game.ball.pos.y - game.paddle1.getCenter().y);
	let dx2 =  Math.abs(game.ball.pos.x - game.paddle2.getCenter().x);
	let dy2 =  Math.abs(game.ball.pos.y - game.paddle2.getCenter().y);

	if (dx1 <= (game.ball.radius + game.paddle1.getHalfWidth()) && dy1 <= (game.ball.radius + game.paddle1.getHalfHeight())){
		game.ball.velocity.x *= -1;
		game.ball.velocity.x += 3;
		game.ball.velocity.y += 3;
	}
	if (dx2 <= (game.ball.radius + game.paddle2.getHalfWidth()) && dy2 <= (game.ball.radius + game.paddle2.getHalfHeight())){
		game.ball.velocity.x += 3;
		game.ball.velocity.y += 3;
		game.ball.velocity.x *= -1;
	}

}

function respawnBall(game) {
	game.ball.pos.x = game.width / 2;
	game.ball.pos.y = game.height / 2;

	game.ball.velocity.x = 0;
	game.ball.velocity.y = 0;

	setTimeout(() => {
		let angle;
		let speed = 12;

		do {
			angle = Math.random() * 2 * Math.PI;
		} while (Math.abs(Math.sin(angle)) < 0.3 || Math.abs(Math.cos(angle)) < 0.3);

		game.ball.velocity.x = Math.cos(angle) * speed;
		game.ball.velocity.y = Math.sin(angle) * speed;
	}, 500);
}


function gameScore(game) {
	if (game.paddle1.score != 5 && game.paddle2.score != 5)
	{
		if (game.ball.pos.x <= -game.ball.radius)
			{
				game.paddle2.score += 1;
				document.getElementById("AIScore").innerHTML = game.paddle2.score;
				respawnBall(game);
			}

			if (game.ball.pos.x >= game.ball.radius + game.width)
			{
				game.paddle1.score += 1;
				document.getElementById("PlayerScore").innerHTML = game.paddle1.score;
				respawnBall(game);
			}
	}
	else
		resetGame(game);
}

function resetGame(game) {
	let winner;
    if (game.mode == 'ai')
        winner = game.paddle1.score === 5 ? "Player" : "AI";
    else if (game.mode == 'multiplayer')
		winner = game.paddle1.score === 5 ? "Player-1" : "Player-2";
    alert(`${winner} wins!`);

    game.paddle1.score = 0;
    game.paddle2.score = 0;
    document.getElementById("PlayerScore").innerHTML = game.paddle1.score;
    document.getElementById("AIScore").innerHTML = game.paddle2.score;

    respawnBall(game);

    game.paddle1.pos = vec2(0, game.height / 2 - game.paddle1.height / 2);
    game.paddle2.pos = vec2(game.width - game.paddle2.width, game.height / 2 - game.paddle2.height / 2);

}

function drawGameFrame(game) {
	game.context.strokeStyle = '#ffff00';

	game.context.beginPath();
	game.context.lineWidth = 15;
	game.context.moveTo(0,0)
	game.context.lineTo(game.width, 0);
	game.context.stroke();


	game.context.beginPath();
	game.context.lineWidth = 15;
	game.context.moveTo(0,game.height)
	game.context.lineTo(game.width, game.height);
	game.context.stroke();

	game.context.beginPath();
	game.context.lineWidth = 15;
	game.context.moveTo(0, 0)
	game.context.lineTo(0, game.height);
	game.context.stroke();

	game.context.beginPath();
	game.context.lineWidth = 15;
	game.context.moveTo(game.width, 0)
	game.context.lineTo(game.width, game.height);
	game.context.stroke();

	game.context.beginPath();
	game.context.lineWidth = 12;
	game.context.moveTo(game.width / 2, 0)
	game.context.lineTo(game.width / 2, game.height);
	game.context.stroke();

	game.context.beginPath();
	game.context.arc(game.width / 2, game.height / 2, 40, 0, Math.PI * 2);
	game.context.stroke();
}

function pauseTable(game){
	game.context.fillStyle = "rgba(0, 0, 0, 0.5)";
	game.context.fillRect(0, 0, game.width, game.height);

	game.context.fillStyle = "#FFFFFF";
	game.context.font = "48px Arial";
	game.context.textAlign = "center";
	game.context.fillText("Game Paused", game.width / 2, game.height / 2);
}
