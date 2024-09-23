async function logoutPage() {
    try {
        const response = await fetch('https://lastdance.com.tr/api/users/logout/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        });
        if (response.ok) {
            ws.close();
            loadPage(selectPage('/'));
            window.history.pushState({}, "", '/');
        } else {
            const errorData = await response.json();
            console.error('Logout failed:', errorData);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}