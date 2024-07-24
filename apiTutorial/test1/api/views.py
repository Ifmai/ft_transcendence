from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from test1.models import Makale
from test1.api.serializers import MakaleSerializer


@api_view(['GET', 'POST'])
def makale_list_create_api_views(request):
	if request.method == 'GET':
		makaleler = Makale.objects.filter(aktif = True) #bu bir nesne değil bu bir query set bir sorgu kümesi var
		#serializer = MakaleSerializer(makaleler) bu hatalı query set veriyoruz çünkü.
		serializer = MakaleSerializer(makaleler, many=True)
		return Response(serializer.data)
	elif request.method == 'POST':
		serializer = MakaleSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response(status=status.HTTP_400_BAD_REQUEST)
