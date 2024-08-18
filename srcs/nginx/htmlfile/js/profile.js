async function profilePage() {
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