const players = [
	{ id: 1, name: "Oyuncu 1", ready: false },
	{ id: 2, name: "Oyuncu 2", ready: false },
	{ id: 3, name: "Oyuncu 3", ready: false },
	{ id: 4, name: "Oyuncu 4", ready: false }
];

const winners = {
	semifinal1: null,
	semifinal2: null,
	final: null
};

function toggleReady(playerId) {
	const player = players.find(p => p.id === playerId);
	player.ready = !player.ready;
	updatePlayerUI(player);
	checkAllReady();
}

function updatePlayerUI(player) {
	const statusElement = document.getElementById(`player${player.id}-status`);
	const readyButton = document.getElementById(`player${player.id}-ready`);
	if (player.ready) {
		statusElement.classList.add('ready');
		readyButton.classList.add('active');
		readyButton.textContent = 'Hazır!';
	} else {
		statusElement.classList.remove('ready');
		readyButton.classList.remove('active');
		readyButton.textContent = 'Hazır';
	}
}

function checkAllReady() {
	if (players.every(player => player.ready)) {
		startTournament();
	}
}

function startTournament() {
	// Simulate semifinal matches
	winners.semifinal1 = Math.random() < 0.5 ? players[0] : players[1];
	winners.semifinal2 = Math.random() < 0.5 ? players[2] : players[3];

	// Update UI for semifinal winners
	document.getElementById('semifinal1').innerHTML = `<h3>${winners.semifinal1.name}</h3>`;
	document.getElementById('semifinal2').innerHTML = `<h3>${winners.semifinal2.name}</h3>`;

	// Simulate final match
	setTimeout(() => {
		winners.final = Math.random() < 0.5 ? winners.semifinal1 : winners.semifinal2;
		document.getElementById('champion').innerHTML = `<h3>Şampiyon: ${winners.final.name}</h3>`;
	}, 2000);
}

async function tour_bracketPage() {
	updatePlayerUI();
}