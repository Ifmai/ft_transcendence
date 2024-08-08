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
            const response = await fetch('https://lastdance.com.tr/api/users/login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: email,
                    password: password
                })
            });
            console.log('Status Code:', response.status);
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }else{
                const responseData = await response.json();
                console.log(responseData);
                localStorage.setItem('token', responseData.token);
                loadPage('../pages/_homepage.html', '../partials/_navbarlogin.html')
            }
        } catch (error) {
            console.error('Error:', error);
        }
    });
}