const getPath = () => window.location.pathname;

function getToken(token) {
    return localStorage.getItem(token);
}

const routers = {
    //'/404' : "../pages/_404.html",
    "/" : "../pages/_homepage.html",
    "/login" : "../pages/_login.html",
    "/register" : "../pages/_register.html",
    '/logout' : '../pages/_logout.html',
    '/profile' : '../pages/_profile.html',
};

const scripts = {
    "../pages/_login.html" : loginPage,
    "../pages/_register.html" : registerPage,
    "../pages/_logout.html": logoutPage,
    "../pages/_profile.html" : profilePage,
};

function selectNavbar(){
    token = getToken('token')
    if(token){
        return "../partials/_navbarlogin.html"
    }
    return "../partials/_navbar.html"
}


function selectPage(){
    const path = getPath();
    const route = routers[path];
    return route;
}

const route = (event) => {
    event = event || window.event;
    event.preventDefault();
    window.history.pushState({}, "", event.target.href);
    loadPage(selectPage(), selectNavbar());
}

const loadPage = async (page, navbar) => {
    console.log("page : ", page);
    try {
        const html = await fetch(page).then((response) => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.text();
        });
        document.getElementById('main-div').innerHTML = html;
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

window.onpopstate = () => loadPage(selectPage(), selectNavbar());
window.route = route;
window.myloadpage = loadPage;
window.mySelectPage = selectPage;

document.addEventListener("DOMContentLoaded", function() {
    console.log("Sayfa Yüklendi.");
    loadPage(selectPage(), selectNavbar());
});