let cleanupFunctions = [];

function getCodeURL(query) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(query);
}

const getPath = () => window.location.pathname;
const only_auth_pages = ["../pages/profile.html", '../pages/public-player.html', '../pages/leaderboard.html', '../pages/chat.html', '../pages/play_select.html', '../pages/tournament.html', '../pages/tournament_bracket.html']
const not_auth_pages = ["../pages/login.html", "../pages/register.html", "../pages/forgot-password.html" , '../pages/new-password.html', "../pages/waitlogin.html"]


function getToken(token) {
    return localStorage.getItem(token);
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}


async function cleanupFunctionsHandle() {
	if (cleanupFunctions.length > 0) {
        cleanupFunctions.forEach(func => func());
        cleanupFunctions = [];
    }
}

async function load_page_check(page) {
	if(only_auth_pages.includes(page) && !getCookie('access_token') && await checkingauth() !== 200){
		loadPage(selectPage('/'));
		window.history.replaceState({}, "", "/");
		return false;
	}
	else if(not_auth_pages.includes(page) && getCookie('access_token')){
		loadPage(selectPage('/'));
		window.history.replaceState({}, "", "/");
		return false;
	}
	else
		return true;
}


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