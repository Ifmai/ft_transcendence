async function logoutPage() {
    try {
        const response = await fetch('https://lastdance.com.tr/api/users/logout/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (response.ok) {
            // Çıkış işlemi başarılı olduğunda yapılacak işlemler
            localStorage.removeItem('token');  // Eğer token'ı localStorage'da saklıyorsanız temizleyin
            loadPage('../pages/_homepage.html', '../partials/_navbar.html');
        } else {
            const errorData = await response.json();
            console.error('Logout failed:', errorData);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}