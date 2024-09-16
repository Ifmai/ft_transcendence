// login.js

async function login(username, password, code_2fa) {
    try {
        const response = await fetch('https://lastdance.com.tr/api/users/jwtlogin/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                password: password,
                code_2fa: code_2fa
            })
        });
        if (response.ok)
            return response;
    } catch (error) {
        console.error(error);
    }
}

async function loginPage() {
    const loginBtn = document.getElementById('login-submit-button');
    const intraBtn = document.getElementById('login-intra-button');
    const twoFactorBtn = document.getElementById("two_factor_auth");
    loginBtn.addEventListener('click', async function(event) {
        event.preventDefault();
        const username = document.getElementById('login-username').value;
        const password = document.getElementById('login-password').value;
        try {
            const response = await login(username, password, "");
            if(response.status == 202){
                document.getElementById('overlay-login').style.display = 'block';
                document.getElementById('qr-popup-login').style.display = 'block';
                twoFactorBtn.addEventListener('click', async function(event) {
                    event.preventDefault();
                    const code = document.getElementById("code-2fa").value;
                    const response_2fca = await login(username, password, code);
                    if(response_2fca.ok){
                        loadPage(selectPage('/'));
                        window.history.pushState({}, "", '/');
                    }else{
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }
                });
            }else if(response.status == 200){
                loadPage(selectPage('/'));
                window.history.pushState({}, "", '/');
            }else{
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
        } catch (error) {
            console.error(error);
        }
    });
    intraBtn.addEventListener('click', async function(event) {
        event.preventDefault();
        try{
            window.location.href = "https://api.intra.42.fr/oauth/authorize?client_id=u-s4t2ud-c7fda387fc96d9bc0bbfb60511719a79b6307a19ad79150bd63c9d67d11033fc&redirect_uri=https%3A%2F%2Flastdance.com.tr%2Fwait&response_type=code";
        } catch (error){
            console.error('Error:', error);
        }
        
    });
}

function getCodeURL() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('code');
}

async function intralogin() {
	try {
		code = getCodeURL();
        const response = await fetch(`https://lastdance.com.tr/api/users/login42/${code}/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });
		if(response.ok){
            loadPage(selectPage('/'));
            window.history.pushState({}, "", '/');
        }else{
            console.log("ananın amı");
        }
	} catch (error) {
		console.error(error);
	}
}

function closePopup2() {
    document.getElementById('overlay-login').style.display = 'none';
    document.getElementById('qr-popup-login').style.display = 'none';
  }