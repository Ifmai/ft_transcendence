from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
# Create your views here.
def login_request(request):
	if request.user.is_authenticated:
		return redirect('home page')
	if request.method == "POST":
		username = request.POST["username"]
		password = request.POST["password"]
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('home page')
		else:
			return render(request, "account/login.html",{
				"error": "username yada paralo yanlış!"
			})
		print(username + " asd " + password)
	else:
		return render(request,"account/login.html")

def register_request(request):
	if request.user.is_authenticated:
		return redirect('home page')
	if request.method == "POST":
		username = request.POST["username"]
		email = request.POST["email"]
		firstname = request.POST["firstname"]
		lastname = request.POST["lastname"]
		password = request.POST["password"]
		repassword = request.POST["repassword"]

		if password == repassword:
			if User.objects.filter(username=username).exists():
				return render(request, "account/register.html", {
					"error":"Bu username'e sahip bir kullanıcı mevcut.",
					"username": "",
					"email": email,
					"firstname": firstname,
					"lastname": lastname,
				})
			elif User.objects.filter(email=email).exists():
				return render(request, "account/register.html", {
					"error":"Bu email'e sahip bir kullanıcı mevcut.",
					"username": username,
					"email": "",
					"firstname": firstname,
					"lastname": lastname,
				})
			else:
				user = User.objects.create_user(username=username, email=email, first_name=firstname, last_name=lastname, password=password)
				user.save()
				return redirect('login')
			
		else:
			return render(request, "account/register.html", {
				"error":"Şifreler aynı değil.",
				"username": username,
				"email": email,
				"firstname": firstname,
				"lastname": lastname,
			})


	return render(request,"account/register.html")

def logout_request(request):
	logout(request)
	return redirect('home page')
