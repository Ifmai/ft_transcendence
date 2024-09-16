function createParticles() {
	const particlesContainer = document.getElementById('particles');
	const particleCount = 50;

	for (let i = 0; i < particleCount; i++) {
		const particle = document.createElement('div');
		particle.classList.add('particle');
		particle.style.left = `${Math.random() * 100}%`;
		particle.style.top = `${Math.random() * 100}%`;
		particle.style.animationDuration = `${Math.random() * 3 + 2}s`;
		particle.style.animationDelay = `${Math.random() * 2}s`;
		particlesContainer.appendChild(particle);

		animateParticle(particle);
	}
}

function animateParticle(particle) {
	const animationDuration = Math.random() * 3000 + 2000;
	const startX = parseFloat(particle.style.left);
	const startY = parseFloat(particle.style.top);
	const endX = Math.random() * 100;
	const endY = Math.random() * 100;

	particle.animate([
		{ left: `${startX}%`, top: `${startY}%` },
		{ left: `${endX}%`, top: `${endY}%` }
	], {
		duration: animationDuration,
		easing: 'linear',
		iterations: Infinity
	});
}

createParticles();