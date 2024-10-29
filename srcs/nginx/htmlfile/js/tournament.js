let tournaments = [];

async function add_tournaments(){
	const tournamentList = document.getElementById('trn-tournamentList');
	tournaments.forEach(tournament => {
		const tournamentItem = document.createElement('div');
		tournamentItem.classList.add('trn-tournament-item');
		tournamentItem.innerHTML = `
			<h2 class="trn-tournament-name id='${tournament.id}'">${tournament.name}</h2>
			<p class="trn-tournament-creator">Created by: ${tournament.creator}</p>
			<a href="#" class="trn-button" id='${tournament.id}'>Join Tournament</a>
		`;
		tournamentList.appendChild(tournamentItem);
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
			const formattedTournaments = data.map(item => ({
				id : item.id,
				name: item.name,
				creator: item.player_aliases
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
			const data = await response.json();
			ws.send(JSON.stringify({
				'type' : 'new_tournament',
				'tournament_id' : data['tournament_id'],
				'creator_name' : nickname
			}));
            window.history.pushState({}, "", `/tournament?tournament=${data['tournament_id']}`);
			await loadPage(selectPage('/tournament'));
		}
		else
			throw new Error(`HTTP error! Status: ${response.status}`);
	} catch (error) {
		console.error(error);
	}
}

async function join_tournament(alliasName, currentTournamentName){
	try {
		const response = await fetch('/api/tournament/', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'Authorization': `Bearer ${getCookie('access_token')}`
			},
			body: JSON.stringify({
                'tournament_id': currentTournamentName,
                'alias_name': alliasName,
				'action' : 'join'
            })
		});
		if(response.ok){
			const data = await response.json();
            window.history.pushState({}, "", `/tournament?tournament=${data['tournament_id']}`);
			await loadPage(selectPage('/tournament'));
		}
		else
			throw new Error(`HTTP error! Status: ${response.status}`);
	} catch (error) {
		console.error(error);
	}
}

async function tournamentPage() {
	let currentTournamentName = '';
	cleanupFunctions.push(cleanTournament);
	await get_tournaments_list();
	const tournamentList = document.getElementById('trn-tournamentList');

	document.getElementById('trn-createTournamentBtn').addEventListener('click', (e) => {
		e.preventDefault();
		document.getElementById('trn-createPopupOverlay').style.display = 'flex';
	});

	tournamentList.addEventListener('click', (e) => {
		if (e.target.classList.contains('trn-button')) {
			e.preventDefault();
			currentTournamentName = e.target.id;
			const tournamentName = e.target.closest('.trn-tournament-item').querySelector('.trn-tournament-name').textContent;
			document.getElementById('trn-joinPopupOverlay').style.display = 'flex';
			document.querySelector('#trn-joinPopupOverlay .trn-popup-title').textContent = `Join Tournament: ${tournamentName}`;
		}
	});

	document.getElementById('trn-joinButton').addEventListener('click', async () => {
		const nickname = document.getElementById('trn-joinNicknameInput').value;
		if(!nickname)
			showPopup('Please enter a nickname');
		else if (nickname.length > 10 || nickname.length < 3)
			showPopup("The alias name must be between 3 and 10 characters long!")
		else if (nickname && currentTournamentName) {
			await join_tournament(nickname, currentTournamentName);
		}
	});

	document.getElementById('trn-createButton').addEventListener('click', async () => {
		const tournamentName = document.getElementById('trn-createTournamentInput').value;
		const nickname = document.getElementById('trn-createNicknameInput').value;
		if (!nickname || !tournamentName)
			showPopup('Please enter both tournament name and nickname');
		else if (nickname.length > 10 || nickname.length < 3)
			showPopup("The tournament name must be between 3 and 10 characters long!")
		else if (nickname.length > 10 || nickname.length < 3)
			showPopup("The alias name must be between 3 and 10 characters long!")
		else if (tournamentName && nickname) {
			document.getElementById('trn-createTournamentInput').value = '';
			document.getElementById('trn-createNicknameInput').value = '';
			await create_tournament(tournamentName, nickname);
		}
	});

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
