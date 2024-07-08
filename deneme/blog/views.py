from django.http import HttpResponse
from django.shortcuts import render
from blog.models import Blog, Catagory

# Create your views here.
def index(request):
	print("BEN BURAYA GİRDİM INDEX.HTML")
	context = {
		"blogs": Blog.objects.filter(is_home=True, is_active=True),
		"catagories" : Catagory.objects.all()
	}
	return render(request, 'blog/index.html', context)

def blogs(request):
	context = {
		"blogs":Blog.objects.filter(is_active=True),
		"catagories" : Catagory.objects.all()
	}
	return render(request, 'blog/blog.html', context)

def blogsDetalist(request, slug):
	blogs = Blog.objects.get(slug=slug)
	cat = Catagory.objects.all(),
	return render(request, 'blog/blogdetalist.html', {
			'blog': blogs,
		}
	)

def blogs_by_catagory(request, slug):
	context = {
		"blogs": Catagory.objects.get(slug=slug).blog_set.filter(is_active=True),
		"catagories" : Catagory.objects.all(),
		"selected" : slug
	}
	return render(request, 'blog/blog.html', context)