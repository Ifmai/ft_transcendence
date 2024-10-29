// Leaderboard data
const leaderboardData = [
];


async function renderLeaderboard(data) {
	const leaderboardBody = document.getElementById('lb-leaderboardBody');
	leaderboardBody.innerHTML = '';
	data.forEach((entry, index) => {
		const row = document.createElement('div');
		row.className = 'lb-leaderboard-row';
		row.innerHTML = `
					<div class="lb-leaderboard-cell lb-rank">${index + 1}</div>
					<div class="lb-leaderboard-cell"><a id="leader_board_link" href="/profile?user=${entry.user}">${entry.user}</a></div>
					<div class="lb-leaderboard-cell lb-score">${entry.point}</div>
				`;
		leaderboardBody.appendChild(row);
	});
}


async function get_data(){
	try {
        const response = await fetch('https://10.11.22.5/api/users/leaderboard/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
				'Authorization': `Bearer ${getCookie('access_token')}`
            },
			credentials: 'include',
        });
		const data = await response.json();
		data.forEach((entry, index) => {
			const data_player = {
				rank: index,
				player : entry.user,
				point: entry.point
			};
			leaderboardData.push(data_player);
		});
		await renderLeaderboard(data)
        return response;
    } catch (error) {
        console.error(error);
        showPopup('Connection error. Please check your internet connection.');
    }
}

async function leaderboardPage() {
	await get_data();
}
