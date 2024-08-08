function getCsrfToken() {
    const name = 'csrftoken='; // CSRF çerezinin adı
    const cookies = document.cookie.split(';'); // Çerezleri ayrıştır

    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i]; // Trimleme yapılmadan alınır
        if (cookie.indexOf(name) === 0) {
            return cookie.substring(name.length, cookie.length); // Token'ı döndür
        }
    }
    return null; // Token bulunamazsa null döndür
}

async function logoutPage() {
    try {
		token = getToken('token')
		csrfToken = getCsrfToken()
		console.log(csrfToken)
		console.log(token);
        const response = await fetch('https://lastdance.com.tr/api/users/logout/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(),
                'Token' : token
            },
        });
        if (response.ok) {
            const data = await response.json();
            console.log('Logout successful:', data);
            localStorage.removeItem('token');
            loadPage('../pages/_homepage.html', '../partials/_navbar.html')
            // Çıkış işlemi başarılı olduğunda yapılacak işlemler
        } else {
            const errorData = await response.json();
            console.error('Logout failed:', errorData);
            // Çıkış işlemi başarısız olduğunda yapılacak işlemler
        }
    } catch (error) {
        console.error('Error:', error);
    }
}