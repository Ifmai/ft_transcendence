from rest_framework import generics, mixins
from user.models import Profil, ProfileComment
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import  GenericViewSet, ModelViewSet
from user.api.serializers import ProfilSerializer, ProfileCommentSerializer, ProfilePhotoSerializer
from user.api.permissions import  SelfProfilOrReadOnly
from rest_framework.filters import SearchFilter


class ProfilViewList(
			mixins.ListModelMixin,
			mixins.RetrieveModelMixin,
			mixins.UpdateModelMixin,
			GenericViewSet):

	#queryset = Profil.objects.all()
	serializer_class = ProfilSerializer
	permission_classes = [IsAuthenticated, SelfProfilOrReadOnly]
	filter_backends = [SearchFilter]
	search_fields = ['=id', '=user__username']

	def get_queryset(self):
		return Profil.objects.filter(user=self.request.user)

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

class ProfilPhotoUpdateView(generics.UpdateAPIView):
	serializer_class = ProfilePhotoSerializer
	permission_classes = [IsAuthenticated]

	def get_object(self):
		profil_object = self.request.user.profil
		return profil_object