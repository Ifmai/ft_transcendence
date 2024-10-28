
let ws = null;
let chat_ws = null;

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
    '/pong-game' : '../pages/pong.html',
    '/local' : '../pages/local.html'
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
    '/play' : playerPage,
    '/tournaments' : tournamentPage,
    '/tournament' : tour_bracketPage,
    '/pong-game' : pongPage,
    '/local' : local_pong
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
    await loadPage(selectPage(getPath()));
}

async function loadPage (page){
    if(page.page != '../pages/pong.html')
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
            console.log("PAGE : ", page.page);
            if(page.page != '../pages/waitlogin.html' && page.page != '../pages/pong.html'){
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
                ponghref.addEventListener('click', async () =>{
                    window.history.pushState({}, "", '/');
                    await loadPage(selectPage('/'));
                });
                navbarToggle.addEventListener('click', () => {
                    navbarLinks.classList.toggle('active');
                });
            }
            else if(page.page == '../pages/waitlogin.html' || page.page == '../pages/pong.html')
                document.getElementById('main-navbar').innerHTML = '';
            const script = page.exec_script;
            if(page.page != "../pages/home_page.html" || script === logoutPage){
                if(script){
                    script();
                }else{
                    throw new Error('Script bulunamadı: ' + page.page + '. Script yok.');
                }
            }
            if (page.page === "../pages/home_page.html") {
                homePage();
            }
            await initWebSocket();
        } catch (error) {
            window.history.pushState({}, "", '/404');
            const newContent = await fetch("../pages/404.html").then(response => response.text());
            document.documentElement.innerHTML = newContent;
        }
    }
}

window.onpopstate = async () => await loadPage(selectPage(getPath()));
window.route = route;

document.addEventListener("DOMContentLoaded", async function() {
    await loadPage(selectPage(getPath()));
});

// window.addEventListener('beforeunload', function (event) {
//     // Veri göndermek için sendBeacon kullanabilirsiniz.
//     const url = 'https://example.com/api/log'; // Hedef URL
//     const data = JSON.stringify({ message: 'Sayfa kapatılıyor' });

//     navigator.sendBeacon(url, data);

//     // İsterseniz burada kullanıcıya bir uyarı mesajı da gösterebilirsiniz.
//     event.returnValue = 'Bu sayfayı kapatmak istediğinize emin misiniz?';
// });

// document.addEventListener('visibilitychange', function() {
//     if (document.visibilityState === 'hidden') {
//         console.log('Sekme kapatıldı veya başka bir sekmeye geçildi.');
//     }
// });
