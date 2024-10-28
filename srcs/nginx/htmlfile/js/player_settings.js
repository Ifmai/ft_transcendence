async function update_photo(formData){
	try {
		const response = await fetch('/api/users/profil_photo/', {
			method: 'PUT',
			headers: {
				'Authorization': `Bearer ${getCookie('access_token')}`  // Token'ı Authorization başlığına ekedik.
			},
			body: formData
		});
		if (response.ok)
			return response;
		else{
			return response.status;
		}
	} catch (error) {
		console.log(error);
	}
}

async function check_2fa(action, code) {
	try {
		const response = await fetch('/api/users/2fcaenable/', {
			method: 'PUT',
			headers: {
				'Content-Type': 'application/json',
				'Authorization': `Bearer ${getCookie('access_token')}`  // Token'ı Authorization başlığına ekedik.
			},
			body: JSON.stringify({
				"code": code,
				"action": action
			})
		});
		if(response.ok)
			return true;
		else
			return false
	} catch (error) {
		console.error(error);
		return false;
	}
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
				showPopup_2fa();
				submitBtn = document.getElementById('twofa-submit');
				cancelBtn = document.getElementById('twofa-cancel');
				submitBtn.addEventListener('click', async function(){
					code = document.getElementById('twofa-code').value;
					statusCode = await check_2fa('check', code)
					if(statusCode == true)
						closePopup();
				});
				cancelBtn.addEventListener('click', function(){
					document.getElementById('pp-twoFactorAuth').checked = false;
					closePopup();
				})
			}else if (action == 'disable')
				document.getElementById('pp-twoFactorAuth').checked = false;
		}
	} catch (error) {
		console.error(error);
		return true;
	}
}

async function getinfo() {
	try {
		url = `/api/users/user_profil/`
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


async function ppSaveChanges() {
	const firstName = document.getElementById('pp-firstName').value;
	const lastName = document.getElementById('pp-lastName').value;
	const city = document.getElementById('pp-city').value;
	const bio = document.getElementById('pp-bio').value;
	const pp_photo = document.getElementById('pp-photo-upload');

	const data_user = await getinfo();
	const data_id = await data_user.json();
	const file = pp_photo.files[0];
	
	try {
		let response_status;
		if(file){
			const formData = new FormData();
			formData.append('photo', file);
			response_status = await update_photo(formData);
	
		}
		const response = await fetch(`/api/users/user_profil/${data_id[0]['id']}/`, {
			method: 'PUT',
			headers: {
				'Content-Type': 'application/json',
				'Authorization': `Bearer ${getCookie('access_token')}`  // Token'ı Authorization başlığına ekedik.
			},
			body: JSON.stringify({
				'user_first_name_update' : firstName,
				'user_last_name_update' : lastName,
				'city' : city,
				'bio' : bio
			})
		});
		if(response.ok || response_status.ok){
			window.history.replaceState({}, "", "/profile");
			await loadPage(selectPage('/profile'));
		}
		//alert('Changes saved successfully!'); kenardan çıkıcak salakça şeye eklencek bu.
	} catch (error) {
		console.error(error);
	}
}

async function ppCancel() {
	await loadPage(selectPage('/profile'));
	window.history.replaceState({}, "", "/profile");
}

async function upload_value(){
	const response = await getinfo();
	try {
		if(response.ok){
			const data = await response.json();
			document.getElementById('pp-avatar-settings').src = data[0]["photo"] || '';
			document.getElementById('pp-firstName').value = data[0]["user_first_name"] || '';
            document.getElementById('pp-lastName').value = data[0]["user_last_name"] || '';
            document.getElementById('pp-city').value = data[0]["city"] || '';
            document.getElementById('pp-bio').value = data[0]["bio"] || '';
            document.getElementById('pp-twoFactorAuth').checked = data[0]['two_factory'] || false;
		}
	} catch (error) {
		console.error(error);
	}
}

async function settingsPage(){
	await upload_value();
	const changeBtn = document.getElementById('pp-submit');
	const cancelBtn = document.getElementById('pp-cancel');
	const twoFactorAuth = document.getElementById('pp-twoFactorAuth').checked;
	cancelBtn.addEventListener('click', async function(event){
		await ppCancel();
	});
	changeBtn.addEventListener('click', async function(event){
		await ppSaveChanges();
	});

	const ppTwoFactorAuthToggle = document.getElementById('pp-twoFactorAuth');
	ppTwoFactorAuthToggle.addEventListener('change', async function() {
		if(this.checked == true)
			action_2fca('enable');
		else
			action_2fca('disable');
		console.log('Two-Factor Authentication:', this.checked ? 'Enabled' : 'Disabled');
	});
}

function showPopup_2fa() {
	document.getElementById('twofa-popup').style.display = 'block';
	document.getElementById('overlay').style.display = 'block';
}

function closePopup() {
	document.getElementById('twofa-popup').style.display = 'none';
	document.getElementById('overlay').style.display = 'none';
}