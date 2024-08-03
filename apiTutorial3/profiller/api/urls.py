from django.urls import path, include
from profiller.api.views import ProfilViewList, ProfilDurumViewsList, ProfilPhotoUpdateView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'kullanici-profilleri', ProfilViewList)
router.register(r'kullanici-durum', ProfilDurumViewsList, basename='durum')


urlpatterns = [
    path('', include(router.urls)),
    path('profil_foto/', ProfilPhotoUpdateView.as_view(), name='profil-foto')
]
