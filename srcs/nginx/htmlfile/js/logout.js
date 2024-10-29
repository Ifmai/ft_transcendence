async function logoutPage() {
    try {
        const response = await fetch('https://10.11.22.5/api/users/logout/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        });
        if (response.ok) {
            ws.close();
            window.history.pushState({}, "", '/');
            await loadPage(selectPage('/'));
        } else {
            const errorData = await response.json();
            console.error('Logout failed:', errorData);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}
