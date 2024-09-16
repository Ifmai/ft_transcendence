async function homePage() {
	const hpBall = document.querySelector('.hp-ball-demo');
	const hpLeftPaddle = document.querySelector('.hp-paddle-left');
	const hpRightPaddle = document.querySelector('.hp-paddle-right');
	let hpBallX = 0;
	let hpBallY = 0;
	let hpBallSpeedX = 2;
	let hpBallSpeedY = 2;

	const hpPongDemo = document.querySelector('.hp-pong-demo');
	const hpMaxX = hpPongDemo.clientWidth - hpBall.clientWidth;
	const hpMaxY = hpPongDemo.clientHeight - hpBall.clientHeight;

	hpBallX += hpBallSpeedX;
	hpBallY += hpBallSpeedY;

	if (hpBallX <= 0 || hpBallX >= hpMaxX) {
		hpBallSpeedX = -hpBallSpeedX;
	}
	if (hpBallY <= 0 || hpBallY >= hpMaxY) {
		hpBallSpeedY = -hpBallSpeedY;
	}

	hpBall.style.left = `${hpBallX}px`;
	hpBall.style.top = `${hpBallY}px`;

	// Simple AI for paddles
	hpLeftPaddle.style.top = `${hpBallY - 30}px`;
	hpRightPaddle.style.top = `${hpBallY - 30}px`;

	requestAnimationFrame(homePage);

}