#from rest_framework.generics import GenericAPIView
#from rest_framework.mixins import ListModelMixin, CreateModelMixin
from kitaplar.models import Kitap, Yorum
from kitaplar.api.serializers import KitapSerializers, YorumSerializers

from rest_framework import generics
from rest_framework.generics import get_object_or_404

from rest_framework import permissions
from kitaplar.api.permission import IsAdminUserOrReadOnly, IsYorumSahibiOrReadOnly
from kitaplar.api.pagination import SmallPagination, LargePagination
from rest_framework.exceptions import ValidationError


class KitapListApiViews(generics.ListCreateAPIView):
	queryset = Kitap.objects.all().order_by('id')
	serializer_class = KitapSerializers
	permission_classes = [IsAdminUserOrReadOnly]
	pagination_class = LargePagination


class KitapDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
	queryset = Kitap.objects.all()
	serializer_class = KitapSerializers
	permission_classes = [IsAdminUserOrReadOnly]


class YorumCreateAPIView(generics.CreateAPIView):
	queryset = Yorum.objects.all()
	serializer_class = YorumSerializers
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]

	def perform_create(self, serializer):
		#path('kitaplar/<int:kitap_pk>/yorum_yap', api_views.YorumCreateAPIView.as_view(), name='yorum-yap'),
		kitap_pk = self.kwargs.get('kitap_pk')
		kitap = get_object_or_404(Kitap, pk=kitap_pk)
		kullanici = self.request.user
		yorumlar = Yorum.objects.filter(kitap=kitap, yorum_sahibi=kullanici)
		if yorumlar.exists():
			raise ValidationError('Bir kitaba bir yorum yapabilirsiniz.')
		else:
			serializer.save(kitap=kitap, yorum_sahibi=kullanici)

class YorumDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
	queryset = Yorum.objects.all()
	serializer_class = YorumSerializers
	permission_classes = [IsYorumSahibiOrReadOnly]


class YorumListAPIView(generics.ListAPIView):
	queryset = Yorum.objects.all()
	serializer_class = YorumSerializers

















""" class KitapListApiViews(ListModelMixin, CreateModelMixin, GenericAPIView):
	#bunları belirlemek zorundayız.
	queryset = Kitap.objects.all()
	serializer_class = KitapSerializers

	#Listelemek İstiyoruz GET
	def get(self, request, *args, **kwargs):
		return self.list(request, *args, **kwargs)

	#Yeni kitap yaratmak istiyorum POST
	def post (self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs) """

