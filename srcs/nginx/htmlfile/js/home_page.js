async function homePage() {
	const hpBall = document.querySelector('.hp-ball-demo');
	const hpLeftPaddle = document.querySelector('.hp-paddle-left');
	const hpRightPaddle = document.querySelector('.hp-paddle-right');
	let hpBallX = 0;
	let hpBallY = 0;
	let hpBallSpeedX = 2;
	let hpBallSpeedY = 2;
	let leftPaddleY = 100; // Sol paddle başlangıç konumu
	let rightPaddleY = 100; // Sağ paddle başlangıç konumu
	const hpPongDemo = document.querySelector('.hp-pong-demo');
	const hpMaxX = hpPongDemo.clientWidth - hpBall.clientWidth;
	const hpMaxY = hpPongDemo.clientHeight - hpBall.clientHeight;

	function updateBall() {
		hpBallX += hpBallSpeedX;
		hpBallY += hpBallSpeedY;

		// Topun duvarlara çarpmasını kontrol et
		if (hpBallX <= 0 || hpBallX >= hpMaxX) {
			hpBallSpeedX = -hpBallSpeedX; // Yön değiştir
		}
		if (hpBallY <= 0 || hpBallY >= hpMaxY) {
			hpBallSpeedY = -hpBallSpeedY; // Yön değiştir
		}

		// Paddle'lara çarpma kontrolü
		if (hpBallX <= 10 && hpBallY + hpBall.clientHeight >= leftPaddleY && hpBallY <= leftPaddleY + hpLeftPaddle.clientHeight) {
			hpBallSpeedX = -hpBallSpeedX;
		}
		if (hpBallX >= hpMaxX - 10 && hpBallY + hpBall.clientHeight >= rightPaddleY && hpBallY <= rightPaddleY + hpRightPaddle.clientHeight) {
			hpBallSpeedX = -hpBallSpeedX;
		}

		hpBall.style.left = `${hpBallX}px`;
		hpBall.style.top = `${hpBallY}px`;
	}

	function updatePaddles() {
		// Sol paddle topun y konumuna göre hareket eder
		if (leftPaddleY + 30 < hpBallY && leftPaddleY < hpMaxY - 60) {
			leftPaddleY += 4; // Aşağı hareket
		} else if (leftPaddleY + 20 > hpBallY && leftPaddleY > 0) {
			leftPaddleY -= 4; // Yukarı hareket
		}

		// Sağ paddle topun y konumuna göre hareket eder
		if (rightPaddleY + 30 < hpBallY && rightPaddleY < hpMaxY - 60) {
			rightPaddleY += 4; // Aşağı hareket
		} else if (rightPaddleY + 20 > hpBallY && rightPaddleY > 0) {
			rightPaddleY -= 4; // Yukarı hareket
		}

		hpLeftPaddle.style.top = `${leftPaddleY}px`;
		hpRightPaddle.style.top = `${rightPaddleY}px`;
	}

	function gameLoop() {
		updateBall();
		updatePaddles();
		requestAnimationFrame(gameLoop);
	}

	gameLoop(); // Oyun döngüsünü başlat
}
