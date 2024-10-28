function AIPlayer(game) {
	if (game.ball.velocity.x > 0)
	{
		if (game.ball.pos.y > game.paddle2.pos.y){
			game.paddle2.pos.y += game.paddle2.velocity.y;

			if (game.paddle2.pos.y + game.paddle2.height >= game.height)
				game.paddle2.pos.y = game.height - game.paddle2.height;
		}

		if (game.ball.pos.y < game.paddle2.pos.y){
			game.paddle2.pos.y -= game.paddle2.velocity.y;

			if (game.paddle2.pos.y + game.paddle2.height <= 0)
				game.paddle2.pos.y = 0;
		}
	}
}
