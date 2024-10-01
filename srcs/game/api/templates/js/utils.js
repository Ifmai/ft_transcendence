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
