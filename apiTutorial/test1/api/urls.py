from django.urls import path, include
from test1.api import views as api_views

#Class Based Views
urlpatterns = [
	path('yazarlar/', api_views.GazeteciListCreateApiViews.as_view(), name='yazar-listesi'),
	path('makaleler/', api_views.MakeleListCreateApiViews.as_view(), name='makale-listesi'),
	path('makaleler/<int:pk>', api_views.MakaleDetailsApiViews.as_view(), name='makale-details'),
]

#Function Based Views
""" urlpatterns = [
	path('makaleler/', api_views.makale_list_create_api_views, name='makale-listesi'),
	path('makaleler/<int:pk>', api_views.makale_details_api_views, name='makale-details'),
] """