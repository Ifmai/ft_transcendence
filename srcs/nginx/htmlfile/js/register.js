// login.js

function registerPage(){
    const registerBtn = document.getElementById('registerBtn');
    registerBtn.addEventListener('click', function(event) {
        const firstName = document.getElementById('register-Fname').value;
        const secondName = document.getElementById('register-Sname').value;
        const username = document.getElementById('register-username').value;
        const email = document.getElementById('register-email').value;
        const pass1 = document.getElementById('register-pass1').value;
        const pass2 = document.getElementById('register-pass2').value;

        console.log('first name:', firstName);
        console.log('second name:', secondName);
        console.log('user name:', username);
        console.log('Email:', email);
        console.log('pass1:', pass1);
        console.log('pass2:', pass2);
        // Burada ek işlemler yapılabilir (örneğin, bir API'ye istek gönderme)
    });
}
