async function registerPage(){
    const registerBtn = document.getElementById('registerBtn');
    registerBtn.addEventListener('click', async function(event) {
        const username = document.getElementById('register-username').value;
        const email = document.getElementById('register-email').value;
        const firt_name = document.getElementById('register-first-name').value;
        const last_name = document.getElementById('register-last-name').value;
        const pass1 = document.getElementById('register-password').value;
        const pass2 = document.getElementById('register-confirm-password').value;

        if(pass1 !== pass2)
             showPopup('Passwords do not match');
        else{
            try {
                const response = await fetch('https://lastdance.com.tr/api/users/register/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
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
                }else
                    showPopup('Registration successful!', true);
                    setTimeout(()=>{
                        loadPage(selectPage('/'));
                    }, 1000);
            } catch (error) {
                console.error('Error:', error);
            }
        }
    });
}
