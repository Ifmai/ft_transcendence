function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // This checks if this cookie string begins with the name we want
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function getRefreshFromUrl() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('refresh');
}

async function forgotPassword() {
    const loginBtn = document.getElementById('refpassword');
    loginBtn.addEventListener('click', async function(event) {
        event.preventDefault();
        const email = document.getElementById('email-ref').value;
		const csrfToken = getCookie('csrftoken');
        console.log('Email:', email);
        try {
            const response = await fetch('https://lastdance.com.tr/api/users/refreshpassword/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
					'X-CSRFToken': csrfToken,
                },
                body: JSON.stringify({
                    'email': email,
                })
            });
            if (response.ok) {
                loadPage('../pages/_homepage.html', '../partials/_navbarlogin.html');
            } else {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    });
}

async function newPasswordPage() {
    const form = document.getElementById('refpassword');
    form.addEventListener('click', async (event) => {
        event.preventDefault();
        const newPassword = document.getElementById('password-new').value;
        const newPassword2 = document.getElementById('password-new-2').value;
        const refresh = getRefreshFromUrl();  // Token'ı URL'den al

        if (newPassword !== newPassword2) {
            alert('Şifreler aynı değil.');
            return;
        }
        try {
            const response = await fetch(`https://lastdance.com.tr/api/users/reset/${refresh}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    new_password: newPassword
                })
            });
            const data = await response.json();
            if (response.ok) {
                alert("Şifre başarıyla sıfırlandı.");
                window.history.pushState({}, "", "/login");
                loadPage(selectPage());
            } else {
                alert("Şifre sıfırlama hatası: " + data.error);
            }
        } catch (error) {
            console.error("Hata:", error);
            alert("Bir hata oluştu.");
        }
    });
}
