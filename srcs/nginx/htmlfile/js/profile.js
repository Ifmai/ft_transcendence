async function profilePage() {
  let firstClick = true;

  document.getElementById('2fa-btn').addEventListener('click', async function() {
      if (firstClick) {
        try {
          const response = await fetch('/api/users/2fcaenable/', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${getCookie('access_token')}`  // Token'ı Authorization başlığına ekedik.
            },
            credentials: 'include',
        });
      
          if (response.ok) {
            const data = await response.json();
            console.log('Profil Bilgileri:', data);
            document.getElementById('qr-code-container').innerHTML = data.qr_svg;
          } else {
            console.log('Profil bilgilerini çekerken bir hata oluştu:', response.status);
          }
        } catch (error) {
          console.error('Profil bilgilerini çekerken bir hata oluştu:', error);
        }
          document.getElementById('overlay').style.display = 'block';
          document.getElementById('qr-popup').style.display = 'block';
          firstClick = false;
          this.textContent = 'Disable 2FA';
      } else {
          alert('2FA disabled.');
          this.textContent = 'Enable 2FA';
          firstClick = true;
      }
    });
  
    try {
      // Profil bilgilerini çekmek için fetch isteği gönder
      const response = await fetch('/api/users/user_profil/', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${getCookie('access_token')}`  // Token'ı Authorization başlığına ekedik.
        },
        credentials: 'include',
    });
  
      if (response.ok) {
        const data = await response.json();
        console.log('Profil Bilgileri:', data);
      } else {
        console.log('Profil bilgilerini çekerken bir hata oluştu:', response.status);
      }
    } catch (error) {
      console.error('Profil bilgilerini çekerken bir hata oluştu:', error);
    }
  }

function closePopup() {
    document.getElementById('overlay').style.display = 'none';
    document.getElementById('qr-popup').style.display = 'none';
}