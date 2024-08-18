// login.js

async function loginPage() {
    const loginBtn = document.getElementById('loginBtn');
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
            } else {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    });
}