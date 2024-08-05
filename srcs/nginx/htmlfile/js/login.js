// login.js

function loginPage(){
    const loginBtn = document.getElementById('loginBtn');
    loginBtn.addEventListener('click', function(event) {
        const email = document.getElementById('email-login').value;
        const password = document.getElementById('password-login').value;

        console.log('Email:', email);
        console.log('Password:', password);
        // Burada ek işlemler yapılabilir (örneğin, bir API'ye istek gönderme)
    });
}