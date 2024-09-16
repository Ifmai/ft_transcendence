const getPath = () => window.location.pathname;
const only_auth_pages = ["../pages/profile.html"]
const not_auth_pages = ["../pages/login.html", "../pages/register.html", "../pages/forgot_password.html" ]

let ws = null;
let chat_ws = null;
//let loadFunctions = []
//let cleanupFunctions = [];

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

async function emptyFunc() {
    console.log("yüklendi tükürdüğüm");
}

//'/404' : "../pages/error.html",
//'/logout' : '../pages/logout.html',
const routers = {
    "/" : "../pages/home_page.html",
    "/login" : "../pages/login.html",
    "/wait" : "../pages/waitlogin.html",
    "/register" : "../pages/register.html", 
    '/profile' : '../pages/public-player.html',
    '/leaderboard': '../pages/leaderboard.html',
    '/chat' : '../pages/chat.html',
    '/forgot-password' : '../pages/_forgot_password.html',
    '/new-password': '../pages/_new_password.html',
    '/logout' : '../pages/home_page.html',
    '/play' : '../pages/play_select.html',
    '/tournament' : '../pages/tournament.html'
};

const scripts ={
    "/login" : loginPage,
    "/register" : registerPage,
    '/logout' : logoutPage,
    '/profile' : profilePage,
    '/chat' : chatPage,
    '/forgot-password' : forgotPassword,
    '/new-password': newPasswordPage,
    '/wait' : intralogin,
    '/leaderboard' : leaderboardPage,
    '/play' : emptyFunc,
    '/tournament' : tournamentPage
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

function selectPage(path){
    console.log("gelen path : ", path);
    const route = routers[path];
    const script = scripts[path];
    return {
        page: route,
        exec_script: script,
    }
}

const route = async (event) => {
    event = event || window.event;
    event.preventDefault();
    window.history.pushState({}, "", event.target.href);
    loadPage(selectPage(getPath()));
}

const loadPage = async (page) => {
    console.log("page : ", page);
    if(only_auth_pages.includes(page.page) && !getCookie('access_token') && await checkingauth() !== 200){
        loadPage('../pages/_homepage.html', '../partials/navbar.html')
        window.history.replaceState({}, "", "/");  // URL'i anasayfa olarak güncelle
    }
    else if(not_auth_pages.includes(page.page) && getCookie('access_token')){
        loadPage('../pages/_homepage.html', '../partials/_navbar.html')
        window.history.replaceState({}, "", "/");  // URL'i anasayfa olarak güncelle
    }
    else{
        try {
            const html = await fetch(page.page).then((response) => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.text();
            });
            document.getElementById('main-div').innerHTML = html;            
            if(page.page != '../pages/waitlogin.html'){
                const navbar = await selectNavbar()
                const navbarhtml = await fetch(navbar).then((response) => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.text();
                });
                document.getElementById('main-navbar').innerHTML = navbarhtml;
                const navbarToggle = document.getElementById('idx-navbar-toggle');
                const navbarLinks = document.getElementById('idx-navbar-links');

                navbarToggle.addEventListener('click', () => {
                    navbarLinks.classList.toggle('active');
                });
            }
            const script = page.exec_script;
            if(page.page != "../pages/home_page.html"){
                if(script){
                    script();
                }else{
                    throw new Error('Sayfa bulunamadı: ' + page.exec_script + '. Script yok.');
                }
            }
            await initWebSocket();
        } catch (error) {
            console.error('Sayfa yüklenirken bir hata oluştu:', error);
            //document.getElementById('main-div').innerHTML = await fetch(routers["/404"]).then(response => response.text());
        }
    }
}

window.onpopstate = () => loadPage(selectPage(getPath()));
window.route = route;

document.addEventListener("DOMContentLoaded", function() {
    console.log("Sayfa Yüklendi.");
    loadPage(selectPage(getPath()));
});


async function initWebSocket() {
    if (ws && ws.readyState === WebSocket.OPEN) {
        console.log('WebSocket zaten açık.');
        return;
    }
    token = getCookie('access_token')
    if(!token) {
        console.log('Kullanıcı oturum açmamış, WebSocket bağlantısı oluşturulmadı.');
        return;
    }

    // Yeni WebSocket bağlantısı oluştur
    ws = new WebSocket(`wss://lastdance.com.tr/ws/friend-list/?token=${getCookie('access_token')}`);
    ws.onopen = function(event) {
        console.log('WebSocket bağlantısı açıldı.');
    };

    ws.onmessage = function(event) {
        const data = JSON.parse(event.data);
        console.log('Gelen veri:', data);
    };

    ws.onclose = function(event) {
        console.log('WebSocket bağlantısı kapandı.');
    };

    ws.onerror = function(event) {
        console.error('WebSocket hata:', event);
    };
}

//WebSocket bağlantısını kapatma fonksiyonu
function closeWebSocket() {
    if (ws) {
        ws.close();
        ws = null;
    }
}


window.addEventListener('beforeunload', () => {
    closeWebSocket();
    closeWebSocket2();
});
