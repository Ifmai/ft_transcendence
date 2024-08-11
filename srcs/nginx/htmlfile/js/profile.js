async function profilePage() {
    try {
      // Profil bilgilerini çekmek için fetch isteği gönder
      const response = await fetch('/api/users/user_profil/', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${getCookie('access_token')}`  // Token'ı Authorization başlığında geçirin
        },
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