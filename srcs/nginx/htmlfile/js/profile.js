async function action_2fca(action) {
  try {
    const response = await fetch('/api/users/2fcaenable/', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${getCookie('access_token')}`  // Token'ı Authorization başlığına ekedik.
      },
      body: JSON.stringify({
        "action": action
      })
    });
    if (response.ok) {
      const data = await response.json();
      document.getElementById('qr-code-container').innerHTML = data.qr_svg;
      if( action == "enable"){
        document.getElementById('overlay').style.display = 'block';
        document.getElementById('qr-popup').style.display = 'block';
        return false;
      }else{
        return true;
      }
    }
  }catch (error) {
    console.log('Profil bilgilerini çekerken bir hata oluştu:', response.status);
    return true;
  }
}

async function profilePage() {
  let firstClick = true;
  const btn2Fa = document.getElementById("2fa-btn");
  btn2Fa.addEventListener('click', async function () {
    if (firstClick) {
      firstClick = await action_2fca("enable");
      this.textContent = 'Disable 2FA';
    } else {
      firstClick = await action_2fca("disable");
      alert('2FA disabled.');
      this.textContent = 'Enable 2FA';
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
      check_data = data[0]["two_factory"];
      firstClick = check_data ? false : true;
      if(firstClick == true)
        btn2Fa.textContent = 'Enable 2FA'
      else
        btn2Fa.textContent = 'Disable 2FA'
      console.log("first click : ", firstClick);
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