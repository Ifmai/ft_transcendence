// login.js

async function registerPage(){
    const registerBtn = document.getElementById('registerBtn');
    registerBtn.addEventListener('click', async function(event) {
        const username = document.getElementById('register-username').value;
        const email = document.getElementById('register-email').value;
        const firt_name = document.getElementById('register-fName').value;
        const last_name = document.getElementById('register-lName').value;
        const pass1 = document.getElementById('register-pass1').value;
        const pass2 = document.getElementById('register-pass2').value;
        csrfToken = getCsrfToken()
        console.log('user name:', username);
        console.log('Email:', email);
        console.log('pass1:', pass1);
        console.log('pass2:', pass2);

        try {
            // API'ye istek gönderme
            const response = await fetch('https://lastdance.com.tr/api/register/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
                body: JSON.stringify({
                    "username": username,
                    "first_name": firt_name,
                    "last_name": last_name,
                    "email": email,
                    "password": pass1
                })
            });

            console.log('Status Code:', response.status);

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const responseData = await response.json();
            console.log(responseData);

            // Giriş başarılı olduğunda yapılacak işlemler buraya eklenebilir

        } catch (error) {
            console.error('Error:', error);
        }
        // Burada ek işlemler yapılabilir (örneğin, bir API'ye istek gönderme)
    });
}
