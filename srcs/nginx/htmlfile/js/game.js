const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const startButton = document.getElementById('startButton');
const player1ScoreElement = document.getElementById('player1Score');
const player2ScoreElement = document.getElementById('player2Score');

let player1Score = 0;
let player2Score = 0;
let player1Y = 250;
let player2Y = 250;
let ballX = 580;
let ballY = 300;
let ballSpeedX = 7;
let ballSpeedY = 7;
const paddleHeight = 100;
const paddleWidth = 10;
const ballSize = 10;
let gameLoop;
let isGameRunning = false;

function drawRect(x, y, width, height, color) {
    ctx.fillStyle = color;
    ctx.fillRect(x, y, width, height);
}

function drawCircle(x, y, radius, color) {
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.arc(x, y, radius, 0, Math.PI * 2, false);
    ctx.fill();
}

function updateGame() {
    ballX += ballSpeedX;
    ballY += ballSpeedY;

    if (ballY < 0 || ballY > canvas.height) {
        ballSpeedY = -ballSpeedY;
    }

    if (ballX < paddleWidth && ballY > player1Y && ballY < player1Y + paddleHeight) {
        ballSpeedX = -ballSpeedX;
    }
    if (ballX > canvas.width - paddleWidth && ballY > player2Y && ballY < player2Y + paddleHeight) {
        ballSpeedX = -ballSpeedX;
    }

    if (ballX < 0) {
        player2Score++;
        resetBall();
    } else if (ballX > canvas.width) {
        player1Score++;
        resetBall();
    }

    player1ScoreElement.textContent = `Player 1: ${player1Score}`;
    player2ScoreElement.textContent = `Player 2: ${player2Score}`;

    drawRect(0, 0, canvas.width, canvas.height, 'rgba(45, 55, 72, 0.5)');
    drawRect(0, player1Y, paddleWidth, paddleHeight, '#3182ce');
    drawRect(canvas.width - paddleWidth, player2Y, paddleWidth, paddleHeight, '#3182ce');
    drawCircle(ballX, ballY, ballSize, '#ed8936');
}

function resetBall() {
    ballX = canvas.width / 2;
    ballY = canvas.height / 2;
    ballSpeedX = -ballSpeedX;
    ballSpeedY = 7;
}

function startGame() {
    if (!isGameRunning) {
        gameLoop = setInterval(updateGame, 1000 / 60);
        startButton.textContent = 'Oyunu Durdur';
        isGameRunning = true;
    } else {
        clearInterval(gameLoop);
        isGameRunning = false;
        startButton.textContent = 'Oyunu Başlat';
    }
}

startButton.addEventListener('click', startGame);

canvas.addEventListener('mousemove', (event) => {
    const rect = canvas.getBoundingClientRect();
    const mouseY = event.clientY - rect.top - paddleHeight / 2;
    player1Y = Math.max(0, Math.min(canvas.height - paddleHeight, mouseY));
});

setInterval(() => {
    if (isGameRunning) {
        const paddleCenter = player2Y + paddleHeight / 2;
        if (paddleCenter < ballY - 35) {
            player2Y += 5;
        } else if (paddleCenter > ballY + 35) {
            player2Y -= 5;
        }
    }
}, 1000 / 60);

drawRect(0, 0, canvas.width, canvas.height, 'rgba(45, 55, 72, 0.5)');

function resizeCanvas() {
    const container = document.querySelector('.game-container');
    const containerWidth = container.clientWidth - 40;
    const scale = containerWidth / canvas.width;

    canvas.style.width = `${containerWidth}px`;
    canvas.style.height = `${canvas.height * scale}px`;
}

window.addEventListener('resize', resizeCanvas);
resizeCanvas();
