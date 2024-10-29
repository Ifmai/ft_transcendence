
async function registerPage(){
    const registerBtn = document.getElementById('registerBtn');
    registerBtn.addEventListener('click', async function(event) {
        const username = document.getElementById('register-username').value;
        const email = document.getElementById('register-email').value;
        const first_name = document.getElementById('register-first-name').value;
        const last_name = document.getElementById('register-last-name').value;
        const pass1 = document.getElementById('register-password').value;
        const pass2 = document.getElementById('register-confirm-password').value;

        const errorMessages = []; // Hata mesajlarını depolamak için bir dizi

        // Alanların doluluğunu kontrol et
        if (!email || !username || !first_name || !last_name || !pass1 || !pass2) {
            errorMessages.push('Please fill in all fields.');
        }
        if (first_name === last_name) {
            errorMessages.push('First name and Last name cannot be the same.');
        }
        if (pass1 !== pass2) {
            errorMessages.push('Passwords do not match.');
        }

        // Eğer hata mesajları varsa, göster
        if (errorMessages.length > 0) {
            showPopup(errorMessages.join('<br>')); // Tüm hata mesajlarını birleştir ve göster
            return; // Kontrolü durdur
        }

        try {
            const response = await fetch('https://10.11.22.5/api/users/register/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    "username": username,
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "password": pass1
                })
            });

            console.log('Status Code:', response.status);
            if (response.ok) {
                showPopup('Registration successful!', true);
                await sleep(2000);
                await loadPage(selectPage('/'));
            }

            if (response.status === 400) {
                const errorData = await response.json();
                console.log('Error Data:', errorData);

                // Hata mesajlarını al
                if (typeof errorData === 'object') {
                    const apiMessagesArray = Object.entries(errorData).flatMap(([key, messages]) =>
                        messages.map(msg => `<div>${msg}</div>`)
                    );
                    const combinedMessages = apiMessagesArray.join('');
                    showPopup(combinedMessages); // API'den gelen hata mesajlarını göster
                } else {
                    console.log('Bilinmeyen hata meydana geldi:', errorData);
                }
            } else if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    });
}
