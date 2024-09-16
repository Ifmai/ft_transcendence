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

async function tournamentPage(){
	// Populate tournament list
	const tourlist = document.getElementById('tournamentList');
	tournaments.forEach(tournament => {
		const tournamentItem = document.createElement('div');
		tournamentItem.classList.add('trn-tournament-item');
		tournamentItem.innerHTML = `
			<h2 class="trn-tournament-name">${tournament.name}</h2>
			<p class="trn-tournament-creator">Created by: ${tournament.creator}</p>
			<a href="#" class="trn-button">Join Tournament</a>
		`;
		tourlist.appendChild(tournamentItem);
	});
	
	// Create Tournament button functionality
	document.getElementById('createTournamentBtn').addEventListener('click', (e) => {
		e.preventDefault();
		alert('Create Tournament functionality to be implemented.');
	});
	
	// Join Tournament button functionality
	tourlist.addEventListener('click', (e) => {
		if (e.target.classList.contains('trn-button')) {
			e.preventDefault();
			const tournamentName = e.target.closest('.trn-tournament-item').querySelector('.trn-tournament-name').textContent;
			alert(`Joining tournament: ${tournamentName}`);
		}
	});
}