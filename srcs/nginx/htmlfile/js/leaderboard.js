// Leaderboard data
const leaderboardData = [
	{ rank: 1, player: "Flynn", score: 10000 },
	{ rank: 2, player: "Tron", score: 9500 },
	{ rank: 3, player: "Quorra", score: 9000 },
	{ rank: 4, player: "Clu", score: 8500 },
	{ rank: 5, player: "Sam", score: 8000 },
	{ rank: 6, player: "Rinzler", score: 7500 },
	{ rank: 7, player: "Zuse", score: 7000 },
	{ rank: 8, player: "Gem", score: 6500 },
	{ rank: 9, player: "Castor", score: 6000 },
	{ rank: 10, player: "Ram", score: 5500 },
];

async function leaderboardPage() {
	// Function to render leaderboard
	function renderLeaderboard(data) {
		const leaderboardBody = document.getElementById('lb-leaderboardBody');
		leaderboardBody.innerHTML = '';
		data.forEach((entry, index) => {
			const row = document.createElement('div');
			row.className = 'lb-leaderboard-row';
			row.innerHTML = `
						<div class="lb-leaderboard-cell lb-rank">${index + 1}</div>
						<div class="lb-leaderboard-cell">${entry.player}</div>
						<div class="lb-leaderboard-cell lb-score">${entry.score}</div>
					`;
			leaderboardBody.appendChild(row);
		});
	}
	
	// Initial render
	//api istek yapan bir fonksiyon.
	renderLeaderboard(leaderboardData);
	
	// Sorting functionality
	let currentSort = { column: 'rank', ascending: true };
	
	document.querySelectorAll('.lb-sort-button').forEach(button => {
		button.addEventListener('click', () => {
			const column = button.dataset.sort;
			if (currentSort.column === column) {
				currentSort.ascending = !currentSort.ascending;
			} else {
				currentSort.column = column;
				currentSort.ascending = true;
			}
	
			leaderboardData.sort((a, b) => {
				if (a[column] < b[column]) return currentSort.ascending ? -1 : 1;
				if (a[column] > b[column]) return currentSort.ascending ? 1 : -1;
				return 0;
			});
	
			renderLeaderboard(leaderboardData);
	
			// Update sort indicators
			document.querySelectorAll('.lb-sort-button').forEach(btn => {
				btn.textContent = btn.textContent.replace(' ▼', '').replace(' ▲', '');
			});
			button.textContent += currentSort.ascending ? ' ▼' : ' ▲';
		});
	});
}