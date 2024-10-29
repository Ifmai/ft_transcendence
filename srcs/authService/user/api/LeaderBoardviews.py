from rest_framework import generics, mixins
from rest_framework.views import APIView
from user.models import Profil, ProfileComment
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import  GenericViewSet, ModelViewSet
from user.api.serializers import LeaderBoardSerializer
from user.api.permissions import  SelfProfilOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser



class LeaderBoardView(generics.ListAPIView):
    serializer_class = LeaderBoardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Profil.objects.exclude(user__username='ChatPolice')
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serialized_data = [self.get_serializer(profil).data for profil in queryset]
        sorted_data = sorted(serialized_data, key=lambda x: x['point'], reverse=True)
        top_10 = sorted_data[:10]
        return Response(top_10)