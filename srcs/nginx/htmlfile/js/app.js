const getPath = () => window.location.pathname;
const only_auth_pages = ["../pages/profile.html", '../pages/public-player.html', '../pages/leaderboard.html', '../pages/chat.html', '../pages/play_select.html', '../pages/tournament.html', '../pages/tournament_bracket.html']
const not_auth_pages = ["../pages/login.html", "../pages/register.html", "../pages/forgot-password.html" , '../pages/new-password.html', "../pages/waitlogin.html"]

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
    console.log("yüklendi aga");
}

const routers = {
    "/" : "../pages/home_page.html",
    "/login" : "../pages/login.html",
    "/wait" : "../pages/waitlogin.html",
    "/register" : "../pages/register.html",
    '/profile' : '../pages/public-player.html',
    '/profile-settings' : '../pages/player-profile.html',
    '/leaderboard': '../pages/leaderboard.html',
    '/chat' : '../pages/chat.html',
    '/forgot-password' : '../pages/forgot-password.html',
    '/new-password': '../pages/new-password.html',
    '/logout' : '../pages/home_page.html',
    '/play' : '../pages/play_select.html',
    '/tournaments' : '../pages/tournament.html',
    '/tournament' : '../pages/tournament_bracket.html',
};

const scripts ={
    "/login" : loginPage,
    "/register" : registerPage,
    '/logout' : logoutPage,
    '/profile' : profilePage,
    '/profile-settings' : settingsPage,
    '/chat' : chatPage,
    '/forgot-password' : forgotPassword,
    '/new-password': newPasswordPage,
    '/wait' : intralogin,
    '/leaderboard' : leaderboardPage,
    '/play' : emptyFunc,
    '/tournaments' : tournamentPage,
    '/tournament' : tour_bracketPage
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
        loadPage(selectPage('/'));
        window.history.replaceState({}, "", "/");
    }
    else if(not_auth_pages.includes(page.page) && getCookie('access_token')){
        loadPage(selectPage('/'));
        window.history.replaceState({}, "", "/");
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
                const ponghref = document.getElementById('logo-click');
                ponghref.addEventListener('click', () =>{
                    loadPage(selectPage('/'));
                    window.history.pushState({}, "", '/');
                });
                navbarToggle.addEventListener('click', () => {
                    navbarLinks.classList.toggle('active');
                });
            }
            const script = page.exec_script;
            if(page.page != "../pages/home_page.html" || script === logoutPage){
                if(script){
                    script();
                }else{
                    throw new Error('Sayfa bulunamadı: ' + page.exec_script + '. Script yok.');
                }
            }
            await initWebSocket();
        } catch (error) {
            console.error('Sayfa yüklenirken bir hata oluştu:', error);
            window.history.pushState({}, "", '/404');
            const newContent = await fetch("../pages/404.html").then(response => response.text());
            document.documentElement.innerHTML = newContent;
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
