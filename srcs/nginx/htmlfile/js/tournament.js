const tournaments = [];

async function get_tournaments_list(){
	try {
		const response = await fetch('/api/tournament/get/', {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json',
				'Authorization': `Bearer ${getCookie('access_token')}`
			}
		});
		data = await response.json();
		console.log("data : ", data);
        const formattedTournaments = data.map(item => ({
			id : item.tournaments_id,
            name: item.name,
            creator: item.creator_user
        }));
        tournaments.push(...formattedTournaments);
	} catch (error) {
		console.error(error);
	}
}

async function create_tournament(tournamentname, nickname){
	try {
		const response = await fetch('/api/tournament/', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'Authorization': `Bearer ${getCookie('access_token')}`
			},
			body: JSON.stringify({
                'tournament_name': tournamentname,
                'alias_name': nickname,
				'action' : 'create'
            })
		});
		if(!response.ok)
			throw new Error(`HTTP error! Status: ${response.status}`);
		else{
			const data = await response.json();
			console.log("Oluştu kanka  : ", data);
		}
	} catch (error) {
		console.error(error);
	}
}

async function add_tournaments(){
	const tournamentList = document.getElementById('trn-tournamentList');
	tournaments.forEach(tournament => {
		const tournamentItem = document.createElement('div');
		tournamentItem.classList.add('trn-tournament-item');
		tournamentItem.innerHTML = `
			<h2 class="trn-tournament-name">${tournament.name}</h2>
			<p class="trn-tournament-creator">Created by: ${tournament.creator}</p>
			<a href="#" class="trn-button" id='${tournament.id}'>Join Tournament</a>
		`;
		tournamentList.appendChild(tournamentItem);
	});
	tournamentList.addEventListener('click', (e) => {
		if (e.target.classList.contains('trn-button')) {
			console.log("tıklanan buton id : ", e.target.id);
			e.preventDefault();
			const tournamentName = e.target.closest('.trn-tournament-item').querySelector('.trn-tournament-name').textContent;
			document.getElementById('trn-joinPopupOverlay').style.display = 'flex';
			document.querySelector('#trn-joinPopupOverlay .trn-popup-title').textContent = `Join Tournament: ${tournamentName}`;
		}
	});
}

async function tournamentPage() {
	await get_tournaments_list();
	await add_tournaments();
	// Create Tournament button functionality
	document.getElementById('trn-createTournamentBtn').addEventListener('click', (e) => {
		e.preventDefault();
		document.getElementById('trn-createPopupOverlay').style.display = 'flex';
	});

	// Join Tournament button functionality

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
	document.getElementById('trn-createButton').addEventListener('click', async () => {
		const tournamentName = document.getElementById('trn-createTournamentInput').value;
		const nickname = document.getElementById('trn-createNicknameInput').value;
		console.log("ismi : ", tournamentName, " nickname : ", nickname);
		if (tournamentName && nickname) {
			await create_tournament(tournamentName, nickname);
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
