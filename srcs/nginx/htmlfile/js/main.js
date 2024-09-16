  // JavaScript for creating grid overlay and animated ping pong balls
  const gridOverlay = document.querySelector('.idx-grid-overlay');
  for (let i = 0; i < 72; i++) {
	  const cell = document.createElement('div');
	  cell.classList.add('idx-grid-cell');
	  gridOverlay.appendChild(cell);
  }

  function createPingPongBall() {
	  const ball = document.createElement('div');
	  ball.classList.add('idx-ping-pong-ball');
	  document.body.appendChild(ball);

	  const startX = Math.random() * window.innerWidth;
	  const endX = Math.random() * window.innerWidth;
	  const duration = Math.random() * 3000 + 2000;

	  ball.style.left = `${startX}px`;
	  ball.style.top = '-20px';

	  ball.animate([
		  { transform: `translate(0, -20px)` },
		  { transform: `translate(${endX - startX}px, ${window.innerHeight + 20}px)` }
	  ], {
		  duration: duration,
		  iterations: Infinity,
		  delay: Math.random() * 2000
	  });
  }

  for (let i = 0; i < 5; i++) {
	  createPingPongBall();
  }

  // Add hover effect to game mode cards
const gameModes = document.querySelectorAll('.idx-game-mode');
gameModes.forEach(mode => {
	mode.addEventListener('mouseenter', () => {
		mode.style.transform = 'scale(1.05)';
	});
	mode.addEventListener('mouseleave', () => {
		mode.style.transform = 'scale(1)';
	});
});

