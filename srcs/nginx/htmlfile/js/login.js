function showPopup(message, success = false) {
    const popup = document.getElementById('popup-message');
    popup.innerHTML = message;

    // Başarılı ise yeşil renk, hata ise kırmızı renk
    popup.style.backgroundColor = success ? 'rgba(72, 187, 120, 0.9)' : 'rgba(220, 38, 38, 0.9)';

    popup.style.display = 'block';

    setTimeout(() => {
        popup.style.display = 'none';
    }, 2000);
}

function showPopup_2fa_login() {
    const popup = document.querySelector('.popup');
    popup.style.display = 'flex'; // Make it visible
}

function closePopup_2fa_login() {
    const popup = document.querySelector('.popup');
    popup.style.display = 'none'; // Hide the popup
}


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
        return response;
    } catch (error) {
        console.error(error);
        showPopup('Connection error. Please check your internet connection.');
    }
}

async function loginPage() {
    const loginBtn = document.getElementById('login-submit-button');
    const intraBtn = document.getElementById('login-intra-button');

    loginBtn.addEventListener('click', async function(event) {
        event.preventDefault();
        const username = document.getElementById('login-username').value;
        const password = document.getElementById('login-password').value;
        try {
            const response = await login(username, password, "");
            console.log("Response status:", response.status);
            if (response.status == 202) {
                showPopup_2fa_login();
                console.log("2FA popup shown");

                document.getElementById('twofa-submit').addEventListener('click', async function() {
                    const code = document.getElementById('twofa-code').value;
                    const response_2fa = await login(username, password, code);
                    console.log("giriş yapmayı denedi");

                    if (response_2fa.ok) {
                        console.log("giriş başarılı");

                        closePopup_2fa_login();
                        showPopup('Login successful!', true);
                        setTimeout(async () => {
                            window.history.pushState({}, "", '/');
                            await loadPage(selectPage('/'));
                        }, 2000);
                    } else {
                        showPopup('Invalid 2FA code. Please try again.');
                    }
                });

                document.getElementById('twofa-cancel').addEventListener('click', function() {
                    closePopup_2fa_login();
                });

            } else if (response.status == 200) {
                showPopup('Login successful!', true);
                console.log("GIRDU");
                setTimeout(async () => {
                    window.history.pushState({}, "", '/');
                    await loadPage(selectPage('/'));
                }, 2000);
            } else if (response.status === 500) {
                showPopup('Server error. Please try again later.');
            } else if (response.status === 401){
                console.log("Authentication failed");
                showPopup('Incorrect username or password. Please try again.');
            }
        } catch (error) {
            console.error(error);
            showPopup('Connection error. Please check your internet connection.');
        }
    });

    intraBtn.addEventListener('click', async function(event) {
        event.preventDefault();
        try {
            window.location.href = "https://api.intra.42.fr/oauth/authorize?client_id=u-s4t2ud-c7fda387fc96d9bc0bbfb60511719a79b6307a19ad79150bd63c9d67d11033fc&redirect_uri=https%3A%2F%2Flastdance.com.tr%2Fwait&response_type=code";
        } catch (error) {
            console.error('Error:', error);
        }
    });
}

async function intralogin() {
    try {
        code = getCodeURL('code');
        const response = await fetch(`https://lastdance.com.tr/api/users/login42/${code}/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });
        if (response.ok) {
            await loadPage(selectPage('/'));
            window.history.pushState({}, "", '/');
        } else if (response.status === 500) {
            showPopup('Sunucu hatası. Lütfen daha sonra tekrar deneyin.');
        } else {
            console.log("login problemi var 42 apida");
        }
    } catch (error) {
        console.error(error);
        showPopup('Connection error. Please check your internet connection.');
    }
}

function closePopup2() {
    document.getElementById('overlay-login').style.display = 'none';
    document.getElementById('qr-popup-login').style.display = 'none';
}
