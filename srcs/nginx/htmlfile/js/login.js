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

            // Yanıtın tüm detaylarını görme
            console.log('Status Code:', response.status);
            console.log('Status Text:', response.statusText);
            console.log('Headers:', [...response.headers.entries()]);

            // Yanıtı JSON olarak işleme
            const responseText = await response.text(); // Yanıt metnini al
            console.log('Response Text:', responseText);

            // JSON parse yaparak veriyi alma
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