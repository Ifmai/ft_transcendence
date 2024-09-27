let tournaments = [];

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

async function get_tournaments_list(){
	try {
		const response = await fetch('/api/tournament/get/', {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json',
				'Authorization': `Bearer ${getCookie('access_token')}`
			}
		});
		if(response.ok){
			data = await response.json();
			console.log("data : ", data);
			const formattedTournaments = data.map(item => ({
				id : item.tournaments_id,
				name: item.name,
				creator: item.creator_user
			}));
			tournaments.push(...formattedTournaments);
			await add_tournaments();
		}else
			throw new Error(`HTTP error! Status: ${response.status}`);
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
		if(response.ok){
			console.log("kanka neden mesela?");
			loadPage(selectPage('/tournament'));
		}
		else
			throw new Error(`HTTP error! Status: ${response.status}`);
	} catch (error) {
		console.error(error);
	}
}

async function tournamentPage() {
	cleanupFunctions.push(cleanTournament);
	await get_tournaments_list();
	
	// Create Tournament button functionality
	document.getElementById('trn-createTournamentBtn').addEventListener('click', (e) => {
		e.preventDefault();
		document.getElementById('trn-createPopupOverlay').style.display = 'flex';
	});

	// Join Tournament button functionality

	// Join Game button functionality
	document.getElementById('trn-joinButton').addEventListener('click', async () => {
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
			//await get_tournaments_list();
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

function cleanTournament(){
	tournaments = [];
}