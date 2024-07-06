from django.http import HttpResponse
from django.shortcuts import render

data = {
	"blogs" : [
		{
			"id": 1,
			"title": "Blog 1",
			"image": "djangop.jpg",
			"is_active": True,
			"is_home": True,
			"content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla vel purus nec nibh aliquam tincidunt. Donec ac erat sit amet felis fermentum efficitur"
		},
		{
			"id": 2,
			"title": "Blog 2",
			"image": "nodejs.jpg",
			"is_active": True,
			"is_home": True,
			"content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla vel purus nec nibh aliquam tincidunt. Donec ac erat sit amet felis fermentum efficitur"
		},
		{
			"id": 3,
			"title": "Blog 3",
			"image": "python.jpg",
			"is_active": True,
			"is_home": True,
			"content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla vel purus nec nibh aliquam tincidunt. Donec ac erat sit amet felis fermentum efficitur"
		},
		{
			"id": 4,
			"title": "Blog 4",
			"image": "sadikturan.jpg",
			"is_active": True,
			"is_home": False,
			"content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla vel purus nec nibh aliquam tincidunt. Donec ac erat sit amet felis fermentum efficitur"
		},
	]
}

# Create your views here.
def index(request):
	context = {
		"blogs": data["blogs"],
	}
	return render(request, 'blog/index.html', context)

def blogs(request):
	context = {
		"blogs": data["blogs"],
	}
	return render(request, 'blog/blog.html', context)

def blogsDetalist(request, id):
	blogs = data["blogs"]
	seletedBlog = [blog for blog in blogs if blog["id"] == id][0]
#	seletedBlog = None
#	for blog in blogs:
#		if blog["id"] == id:
#			seletedBlog = blog
#			break
	return render(request, 'blog/blogdetalist.html', {
			'blog': seletedBlog
		}
	)

