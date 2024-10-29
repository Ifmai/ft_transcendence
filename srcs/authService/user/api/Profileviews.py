from rest_framework import generics, mixins
from django.conf import settings
from django.http import HttpResponse, Http404
import os
from rest_framework.views import APIView
from user.models import Profil, ProfileComment
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import  GenericViewSet, ModelViewSet
from user.api.serializers import ProfilSerializer, ProfileUpdateSerializer, ProfileCommentSerializer, ProfilePhotoSerializer
from user.api.permissions import  SelfProfilOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

class ProfilViewList(
			mixins.ListModelMixin,
			mixins.RetrieveModelMixin,
			mixins.UpdateModelMixin,
			GenericViewSet):

	permission_classes = [IsAuthenticated, SelfProfilOrReadOnly]

	def get_queryset(self):
			username = self.kwargs.get('username', None)  # URL'den username'i alıyoruz
			print(f"Username from kwargs: {username}")
			if username:
				return Profil.objects.filter(user__username=username)
			return Profil.objects.filter(user=self.request.user)

	def get_serializer_class(self):
		if self.request.method in ['PUT', 'PATCH']:
			profil = self.get_object()
			if profil.user == self.request.user:
				return ProfileUpdateSerializer
			else:
				raise PermissionDenied("Sadece kendi profilinizi düzenleyebilirsiniz.")
		return ProfilSerializer

class ProfilCommentViewList(ModelViewSet):
	serializer_class = ProfileCommentSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		queryset = ProfileComment.objects.all()
		user_name = self.request.query_params.get('username')
		if user_name is not None:
			queryset = queryset.filter(user_profil__user__username=user_name)
		return queryset

	def perform_create(self, serializer):
		user_profil = self.request.user.profil
		serializer.save(user_profil=user_profil)

class ProfilPhotoUpdateView(generics.UpdateAPIView,):
	serializer_class = ProfilePhotoSerializer
	permission_classes = [IsAuthenticated]
	parser_classes = [JSONParser, MultiPartParser, FormParser]

	def put(self, request, *args, **kwargs):
		profil_object = self.get_object()
		if 'photo' in request.FILES:
			profil_object.photo = request.FILES['photo']
			profil_object.save()
		return Response({'status': 'profile picture updated'})

	def get_object(self):
		profil_object = self.request.user.profil
		return profil_object

def serve_dynamic_image(request, filename):
    ROOT = settings.STATICFILES_DIRS[0]
    image_path = os.path.join(ROOT, 'images', filename)

    if os.path.exists(image_path):
        with open(image_path, 'rb') as f:
            return HttpResponse(f.read(), content_type="image/jpeg")  # Veya uygun olan başka bir tür
    else:
        raise Http404("Image not found")

def serve_dynamic_media(request, filename):
    ROOT = settings.MEDIA_ROOT
    image_path = os.path.join(ROOT, 'profil_photo', filename)


    if os.path.exists(image_path):
        with open(image_path, 'rb') as f:
            return HttpResponse(f.read(), content_type="image/jpeg")  # Veya uygun olan başka bir tür
    else:
        raise Http404("Image not found")
