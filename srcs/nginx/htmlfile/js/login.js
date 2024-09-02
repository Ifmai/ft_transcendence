// login.js

async function loginPage() {
    const loginBtn = document.getElementById('loginBtn');
    const intraBtn = document.getElementById('loginIntraBtn');
    loginBtn.addEventListener('click', async function(event) {
        event.preventDefault();
        const email = document.getElementById('email-login').value;
        const password = document.getElementById('password-login').value;
        console.log('Email:', email);
        console.log('Password:', password);
        try {
            // API'ye istek gönderme
            const response = await fetch('https://lastdance.com.tr/api/users/jwtlogin/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: email,
                    password: password
                })
            });

            if (response.ok) {
                loadPage('../pages/_homepage.html', '../partials/_navbarlogin.html');
                window.history.pushState({}, "", '/');
            } else {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
        } catch (error) {
            console.error('Error:', error);
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
		if(response.ok)
			loadPage("../pages/_homepage.html");
            window.history.pushState({}, "", '/');
	} catch (error) {
		console.error(error);
	}
}
