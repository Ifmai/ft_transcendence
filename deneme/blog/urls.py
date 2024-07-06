from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='home page'),
	path('index', views.index, name='home page'),
	path('blog', views.blogs, name='blog page'),
	path('blog/<int:id>', views.blogsDetalist, name='blog detalist page'),
]