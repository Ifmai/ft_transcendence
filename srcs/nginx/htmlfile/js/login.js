// login.js

async function loginPage() {
    const loginBtn = document.getElementById('loginBtn');
    loginBtn.addEventListener('click', async function(event) {
        // Formun varsayılan submit davranışını engelle
        event.preventDefault();

        const email = document.getElementById('email-login').value;
        const password = document.getElementById('password-login').value;

        console.log('Email:', email);
        console.log('Password:', password);

        try {
            // API'ye istek gönderme
            const response = await fetch('https://lastdance.com.tr/api/rest-auth/login/', {
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
            }

            const responseData = await response.json();
            console.log(responseData);
            localStorage.setItem('token', responseData.key);

            // Giriş başarılı olduğunda yapılacak işlemler buraya eklenebilir

        } catch (error) {
            console.error('Error:', error);
        }
    });
}