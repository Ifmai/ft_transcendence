const getPath = () => window.location.pathname;
const only_auth_pages = ["../pages/_profile.html"]
const not_auth_pages = ["../pages/_login.html", "../pages/_register.html", "../pages/_forgot_password.html" ]


async function checkingauth() {
	try {
		const response = await fetch('https://lastdance.com.tr/api/users/whois/', {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json',
			}
		});
		return response.status
	} catch (error) {
        console.log('errrora düşüyorum geldim.');
		return 500;
	}
}


function getToken(token) {
    return localStorage.getItem(token);
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}


const routers = {
    '/404' : "../pages/_404.html",
    "/" : "../pages/_homepage.html",
    "/login" : "../pages/_login.html",
    "/wait" : "../pages/_waitlogin.html",
    "/register" : "../pages/_register.html",
    '/logout' : '../pages/_logout.html',
    '/profile' : '../pages/_profile.html',
    '/forgot-password' : '../pages/_forgot_password.html',
    '/new-password': '../pages/_new_password.html',
};

const scripts = {
    "../pages/_login.html" : loginPage,
    "../pages/_register.html" : registerPage,
    "../pages/_logout.html": logoutPage,
    "../pages/_profile.html" : profilePage,
    "../pages/_forgot_password.html" : forgotPassword,
    "../pages/_new_password.html" : newPasswordPage,
    "../pages/_waitlogin.html" : intralogin,
};

async function selectNavbar(){
    token = getCookie('access_token')
    if(token)
        return "../partials/_navbarlogin.html"
    else{
        if(await checkingauth() == 200){
            return "../partials/_navbarlogin.html"
        }
        else{
            return "../partials/_navbar.html"
        }
    }
}

function selectPage(){
    const path = getPath();
    const route = routers[path];
    return route;
}

const route = async (event) => {
    event = event || window.event;
    event.preventDefault();
    window.history.pushState({}, "", event.target.href);
    loadPage(selectPage());
}

const loadPage = async (page) => {
    console.log("page : ", page);
    if(only_auth_pages.includes(page) && !getCookie('access_token') && await checkingauth() !== 200){
        loadPage('../pages/_homepage.html', '../partials/navbar.html')
        window.history.replaceState({}, "", "/");  // URL'i anasayfa olarak güncelle
    }
    else if(not_auth_pages.includes(page) && getCookie('access_token')){
        loadPage('../pages/_homepage.html', '../partials/_navbar.html')
        window.history.replaceState({}, "", "/");  // URL'i anasayfa olarak güncelle
    }
    else{
        try {
            const html = await fetch(page).then((response) => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.text();
            });
            document.getElementById('main-div').innerHTML = html;
            const navbar = await selectNavbar()
            const navbarhtml = await fetch(navbar).then((response) => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.text();
            });
            document.getElementById('main-navbar').innerHTML = navbarhtml;
            if(page != '../pages/_homepage.html'){
                const script = scripts[page];
                if(script){
                    script();
                }else{
                    throw new Error('Sayfa bulunamadı: ' + page);
                }
            }
        } catch (error) {
            console.error('Sayfa yüklenirken bir hata oluştu:', error);
            // Hata durumunda varsayılan 404 sayfasına yönlendirme
            document.getElementById('main-div').innerHTML = await fetch(routers["/404"]).then(response => response.text());
        }
    }
}

window.onpopstate = () => loadPage(selectPage());
window.route = route;

document.addEventListener("DOMContentLoaded", function() {
    console.log("Sayfa Yüklendi.");
    loadPage(selectPage());
});