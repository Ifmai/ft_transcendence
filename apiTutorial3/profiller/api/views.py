from rest_framework import generics, mixins
from rest_framework.viewsets import  GenericViewSet, ModelViewSet #ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from profiller.models import Profil, ProfilDurum
from profiller.api.serializers import ProfilSerializer, ProfilDurunSerializer, ProfilPhotoSerializer
from profiller.api.permissions import KendiProfiliOrReadOnly, DurumSahibiOrReadOnly


class ProfilViewList(
            mixins.ListModelMixin,
            mixins.RetrieveModelMixin,
            mixins.UpdateModelMixin,
            GenericViewSet):
    
    queryset = Profil.objects.all()
    serializer_class = ProfilSerializer
    permission_classes = [KendiProfiliOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ['=sehir', '=user__username', '=id']


class ProfilDurumViewsList(ModelViewSet):
    serializer_class = ProfilDurunSerializer
    permission_classes = [IsAuthenticated, DurumSahibiOrReadOnly]

    def get_queryset(self):
        queryset = ProfilDurum.objects.all()
        user_name = self.request.query_params.get('username')
        if user_name is not None:
            queryset = queryset.filter(user_profil__user__username=user_name)
        return queryset

    def perform_create(self, serializer):
        user_profil = self.request.user.profl
        serializer.save(user_profil=user_profil)

class ProfilPhotoUpdateView(generics.UpdateAPIView):
    serializer_class = ProfilPhotoSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        profil_nesnesi = self.request.user.profil
        return profil_nesnesi