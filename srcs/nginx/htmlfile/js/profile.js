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
			url = `/api/users/user_profil/${username}`
			console.log("selam kanka buradayım ilk if ");
		}
		else{
			console.log("selam kanka buradayım ");
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
			console.log("gelen data : ", data);
			//window.history.replaceState({}, "", `/profile?user=${data[0]['user']}`);
			const userProfile = document.getElementById('player-profile');
			const nameLabel = document.getElementById('pub-profile-name');
			const locLabel = document.getElementById('pub-profile-location');
			const bioLabel = document.getElementById('pub-profile-bio');
			const photoLabel = document.getElementById('pub-profile-photo');
			const wincount = document.getElementById('profile-win');
			const losecount = document.getElementById('profile-lose');
			const kdacount = document.getElementById('profile-kda');
			const champcount = document.getElementById('profile-champ');
	
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
		} else {
			console.log('Profil bilgilerini çekerken bir hata oluştu:', response.status);
		}
	} catch (error) {
		console.error(error);
	}	
}