from django.urls import path, include
from test1.api import views as api_views

urlpatterns = [
	path('makaleler/', api_views.makale_list_create_api_views, name='makale-listesi'),
]