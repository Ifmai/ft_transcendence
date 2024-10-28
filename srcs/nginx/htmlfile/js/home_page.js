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
	console.log("BURADASDASDASDASDASDASDASD");
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
		if (hpBallX <= 10 && hpBallY >= leftPaddleY && hpBallY <= leftPaddleY + 60) {
			hpBallSpeedX = -hpBallSpeedX;
		}
		if (hpBallX >= hpMaxX - 10 && hpBallY >= rightPaddleY && hpBallY <= rightPaddleY + 60) {
			hpBallSpeedX = -hpBallSpeedX;
		}

		hpBall.style.left = `${hpBallX}px`;
		hpBall.style.top = `${hpBallY}px`;
	}

	function updatePaddles() {
		// Sol paddle topun y konumuna göre hareket eder
		if (leftPaddleY + 30 < hpBallY) {
			leftPaddleY += 2; // Aşağı hareket
		} else if (leftPaddleY + 30 > hpBallY) {
			leftPaddleY -= 2; // Yukarı hareket
		}

		// Sağ paddle topun y konumuna göre hareket eder
		if (rightPaddleY + 30 < hpBallY) {
			rightPaddleY += 2; // Aşağı hareket
		} else if (rightPaddleY + 30 > hpBallY) {
			rightPaddleY -= 2; // Yukarı hareket
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
