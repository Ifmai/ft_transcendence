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
            const response = await fetch('https://lastdance.com.tr/api/users/register/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken(),
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
            loadPage('../pages/_login.html', '../partials/_navbar.html')
        } catch (error) {
            console.error('Error:', error);
        }
    });
}


async function profilePage() {
    try {
      // Profil bilgilerini çekmek için fetch isteği gönder
      const response = await fetch('/api/users/user_profil/', {
        method: 'GET',
        credentials: 'include',  // Eğer token'lar HttpOnly cookie'de ise include et
      });
  
      // Eğer istek başarılıysa, JSON formatında veriyi al
      if (response.ok) {
        const data = await response.json();
        console.log('Profil Bilgileri:', data);
        
        // Profil bilgilerini kullanarak UI'ı güncelle
        // Örneğin: document.getElementById('username').textContent = data.username;
      } else if (response.status === 401) {
        console.log('Oturumunuz sona erdi, lütfen tekrar giriş yapın.');
        // Giriş sayfasına yönlendirme yapabilirsin
        window.location.href = '/login';
      } else {
        console.log('Profil bilgilerini çekerken bir hata oluştu:', response.status);
      }
    } catch (error) {
      console.error('Profil bilgilerini çekerken bir hata oluştu:', error);
    }
  }