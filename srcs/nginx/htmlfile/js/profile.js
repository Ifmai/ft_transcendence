function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function getCodeURL(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}
async function action_2fca(action) {
	try {
		const response = await fetch('/api/users/2fcaenable/', {
			method: 'PUT',
			headers: {
				'Content-Type': 'application/json',
				'Authorization': `Bearer ${getCookie('access_token')}`  // Token'ı Authorization başlığına ekedik.
			},
			body: JSON.stringify({
				"action": action
			})
		});
		if (response.ok) {
			const data = await response.json();
			document.getElementById('qr-code-container').innerHTML = data.qr_svg;
			if (action == "enable") {
				document.getElementById('overlay').style.display = 'block';
				document.getElementById('qr-popup').style.display = 'block';
				return false;
			} else {
				return true;
			}
		}
	} catch (error) {
		console.log('Profil bilgilerini çekerken bir hata oluştu:', response.status);
		return true;
	}
}

async function getProfile() {
	try {
		const username = getCodeURL('user');
		let url;
		if (username){
			url = `/api/users/user_profil/other/${username}`
		}
		else{
			url = `/api/users/user_profil/`
			const profileHeader = document.querySelector('.pub-profile-header');
   			const settingsLink = `
				<a href="/profile-settings" class="pub-settings-link">
					<i class="fas fa-cog"></i>
				</a>
			`;
			profileHeader.innerHTML += settingsLink;
		}
		const response = await fetch(url, {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json',
				'Authorization': `Bearer ${getCookie('access_token')}`  // Token'ı Authorization başlığına ekedik.
			},
			credentials: 'include',
		});
		if (response.ok)
			return response;
		else{
			return response.status;
		}
	} catch (error) {
		return error;
	}
}

async function profilePage() {
	const response = await getProfile();
	try {
		if (response.ok) {
			const data = await response.json();
			const userProfile = document.getElementById('player-profile');
			const nameLabel = document.getElementById('pub-profile-name');
			const locLabel = document.getElementById('pub-profile-location');
			const bioLabel = document.getElementById('pub-profile-bio');
			const photoLabel = document.getElementById('pub-profile-photo');
			const wincount = document.getElementById('profile-win');
			const losecount = document.getElementById('profile-lose');
			const kdacount = document.getElementById('profile-kda');
			const champcount = document.getElementById('profile-champ');

			const matchHistory = await getMatchHistory();
			if (matchHistory) {
                renderMatchHistory(matchHistory);
            }
			const win = parseInt(data[0]["wins"]);
			const lose = parseInt(data[0]["losses"]);
			const percentage = win / (win + lose) * 100;
			userProfile.textContent = "Profile " + data[0]["user"];
			nameLabel.textContent = data[0]["user_first_name"] + " " + data[0]["user_last_name"];
			locLabel.textContent = "📍 " + data[0]["city"];
			bioLabel.textContent = data[0]["bio"];
			photoLabel.src = data[0]["photo"];
			wincount.textContent = win;
			losecount.textContent = lose;
			kdacount.textContent = isNaN(percentage) ? "0%" : percentage.toFixed(1) + "%";
			champcount.textContent = data[0]["championships"];
			createWinLossChart(win, lose);
		} else {
			console.log('Profil bilgilerini çekerken bir hata oluştu:', response.status);
		}
	} catch (error) {
		console.error(error);
	}
}

function createWinLossChart(wins, losses) {
    // Check if we are on the player profile page
	const chartElement = document.getElementById('winLossChart');
	chartElement.width = 200; // Set the width
	chartElement.height = 200;
	if (!chartElement) {
		console.error("Canvas element not found");
		return;
	}
	const ctx = chartElement.getContext('2d');
	new Chart(ctx, {
		type: 'pie',
		data: {
			labels: ['Wins', 'Losses'],
			datasets: [{
				data: [wins, losses],
				backgroundColor: [
					'rgba(95, 255, 145, 0.8)',
					'rgba(255, 60, 90, 0.8)'
				],
				borderColor: [
					'rgba(104, 211, 145, 1)',
					'rgba(252, 129, 129, 1)'
				],
				borderWidth: 1
			}]
		},
		options: {
			responsive: true,
			plugins: {
				legend: {
					position: 'bottom',
				}
			}
		}
	});
}


async function getMatchHistory() {
    try {
		const username = getCodeURL('user');
		let url;
		if(username){
			url = `/api/tournament/match-history/${username}`
		}
		else{
			url = `/api/tournament/match-history/`
		}
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${getCookie('access_token')}`
            },
            credentials: 'include',
        });
        if (response.ok) {
            return await response.json();
        } else {
            console.log('Failed to fetch match history:', response.status);
            return null;
        }
    } catch (error) {
        console.error('Error fetching match history:', error);
        return null;
    }
}

function renderMatchHistory(matches) {
    const container = document.getElementById('match-history-container');
    container.innerHTML = ''; // Clear existing content

    matches.forEach(match => {
        const matchElement = document.createElement('div');
        matchElement.className = 'match-history-item';

        const players = match.players.map((player, index) => {
            const result = player.won ? 'winner' : 'loser';
            if  (index === 0) {
                // If there's an odd number of players and this is the last player
                return `
                    <div class="player ${result}">
                        <img src="${player.player.photo}" alt="${player.player.user}" class="player-avatar">
                        <span class="player-name"><a id="leader_board_link" href="/profile?user=${player.player.user}">${player.player.user}</a></span>
                        <span class="player-score">${player.score}</span>
                    </div>
                `;
            } else {
                // For even or the other players
                return `
                    <div class="player ${result}">
                        <span class="player-score">${player.score}</span>
                        <span class="player-name"><a id="leader_board_link" href="/profile?user=${player.player.user}">${player.player.user}</a></span>
                        <img src="${player.player.photo}" alt="${player.player.user}" class="player-avatar">
                    </div>
                `;
            }
        }).join('');

        matchElement.innerHTML = `
            <div class="match-players">${players}</div>
        `;

        container.appendChild(matchElement);
    });
}
