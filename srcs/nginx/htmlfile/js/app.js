
let ws = null;
let chat_ws = null;

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
    await cleanupFunctionsHandle();
    const truePage = await load_page_check(page.page);
    if(truePage){
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
                    throw new Error('Script bulunamadı: ' + page.page + '. Script yok.');
                }
            }
            await initWebSocket();
        } catch (error) {
            window.history.pushState({}, "", '/404');
            const newContent = await fetch("../pages/404.html").then(response => response.text());
            document.documentElement.innerHTML = newContent;
        }
    }
}

window.onpopstate = () => loadPage(selectPage(getPath()));
window.route = route;

document.addEventListener("DOMContentLoaded", function() {
    loadPage(selectPage(getPath()));
});