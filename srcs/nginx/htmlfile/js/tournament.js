const tournaments = [
	{ name: "TRON Masters", creator: "GridMaster" },
	{ name: "Neon Showdown", creator: "LightCycle" },
	{ name: "Disc Wars", creator: "Rinzler" },
	{ name: "Bit Bash", creator: "CLU" },
	{ name: "ISO Challenge", creator: "Quorra" },
	{ name: "End of Line Club", creator: "Zuse" },
	{ name: "Disc Wars", creator: "Rinzler" },
	{ name: "Bit Bash", creator: "CLU" },
	{ name: "ISO Challenge", creator: "Quorra" },
	{ name: "Disc Wars", creator: "Rinzler" },
	{ name: "Bit Bash", creator: "CLU" },
	{ name: "ISO Challenge", creator: "Quorra" },
	{ name: "Disc Wars", creator: "Rinzler" },
	{ name: "Bit Bash", creator: "CLU" },
	{ name: "ISO Challenge", creator: "Quorra" },
	{ name: "Disc Wars", creator: "Rinzler" },
	{ name: "Bit Bash", creator: "CLU" },
	{ name: "ISO Challenge", creator: "Quorra" },
	{ name: "Disc Wars", creator: "Rinzler" },
	{ name: "Bit Bash", creator: "CLU" },
	{ name: "ISO Challenge", creator: "Quorra" },
	{ name: "Disc Wars", creator: "Rinzler" },
	{ name: "Bit Bash", creator: "CLU" },
	{ name: "ISO Challenge", creator: "Quorra" },
	{ name: "Disc Wars", creator: "Rinzler" },
	{ name: "Bit Bash", creator: "CLU" },
	{ name: "ISO Challenge", creator: "Quorra" },
	{ name: "Disc Wars", creator: "Rinzler" },
	{ name: "Bit Bash", creator: "CLU" },
	{ name: "ISO Challenge", creator: "Quorra" }
];

async function tournamentPage() {

	const tournamentList = document.getElementById('trn-tournamentList');
	tournaments.forEach(tournament => {
		const tournamentItem = document.createElement('div');
		tournamentItem.classList.add('trn-tournament-item');
		tournamentItem.innerHTML = `
			<h2 class="trn-tournament-name">${tournament.name}</h2>
			<p class="trn-tournament-creator">Created by: ${tournament.creator}</p>
			<a href="#" class="trn-button">Join Tournament</a>
		`;
		tournamentList.appendChild(tournamentItem);
	});

	// Create Tournament button functionality
	document.getElementById('trn-createTournamentBtn').addEventListener('click', (e) => {
		e.preventDefault();
		document.getElementById('trn-createPopupOverlay').style.display = 'flex';
	});

	// Join Tournament button functionality
	tournamentList.addEventListener('click', (e) => {
		if (e.target.classList.contains('trn-button')) {
			e.preventDefault();
			const tournamentName = e.target.closest('.trn-tournament-item').querySelector('.trn-tournament-name').textContent;
			document.getElementById('trn-joinPopupOverlay').style.display = 'flex';
			document.querySelector('#trn-joinPopupOverlay .trn-popup-title').textContent = `Join Tournament: ${tournamentName}`;
		}
	});

	// Join Game button functionality
	document.getElementById('trn-joinButton').addEventListener('click', () => {
		const nickname = document.getElementById('trn-joinNicknameInput').value;
		if (nickname) {
			alert(`Joining tournament with nickname: ${nickname}`);
			document.getElementById('trn-joinPopupOverlay').style.display = 'none';
			document.getElementById('trn-joinNicknameInput').value = '';
		} else {
			alert('Please enter a nickname');
		}
	});

	// Create Tournament button functionality
	document.getElementById('trn-createButton').addEventListener('click', () => {
		const tournamentName = document.getElementById('trn-createTournamentInput').value;
		const nickname = document.getElementById('trn-createNicknameInput').value;
		if (tournamentName && nickname) {
			alert(`Creating tournament: ${tournamentName} with nickname: ${nickname}`);
			document.getElementById('trn-createPopupOverlay').style.display = 'none';
			document.getElementById('trn-createTournamentInput').value = '';
			document.getElementById('trn-createNicknameInput').value = '';
		} else {
			alert('Please enter both tournament name and nickname');
		}
	});

	// Close popup when clicking outside
	document.querySelectorAll('.trn-popup-overlay').forEach(overlay => {
		overlay.addEventListener('click', (e) => {
			if (e.target === overlay) {
				overlay.style.display = 'none';
			}
		});
	});
}
