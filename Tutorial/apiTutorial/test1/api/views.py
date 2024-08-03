from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from test1.models import Makale, Gazateci
from test1.api.serializers import MakaleSerializer, GazetiSerializer

#api class views
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404


class GazeteciListCreateApiViews(APIView):
	def get(self, request):
		yazarlar = Gazateci.objects.all() #bu bir nesne değil bu bir query set bir sorgu kümesi var
		serializer = GazetiSerializer(yazarlar, many=True, context={'request': request})
		return Response(serializer.data)


	def post(self, request):
		serializer = GazetiSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MakeleListCreateApiViews(APIView):
	def get(self, request):
		makaleler = Makale.objects.filter(aktif = True) #bu bir nesne değil bu bir query set bir sorgu kümesi var
		serializer = MakaleSerializer(makaleler, many=True)
		return Response(serializer.data)


	def post(self, request):
		serializer = MakaleSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MakaleDetailsApiViews(APIView):

	def get_object(self, pk):
		makale_instance = get_object_or_404(Makale, pk=pk)
		return makale_instance

	def get(self,request, pk):
		makale = self.get_object(pk=pk)
		serializer = MakaleSerializer(makale)
		return Response(serializer.data)
	
	def put(self, request, pk):
		makale = self.get_object(pk=pk)
		serializer = MakaleSerializer(makale, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk):
		makale = self.get_object(pk=pk)
		makale.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)


#Api function
""" @api_view(['GET', 'POST'])
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
 

@api_view(['GET', 'PUT', 'DELETE'])
def makale_details_api_views(request, pk):
	try:
		makale_instance = Makale.objects.get(pk=pk)
	except Makale.DoesNotExist:
		return Response({
			'errors': {
				'code':404,
				'message': f'Böyle bir id ({pk}) ile uygun makale bulunamadı.'
			}
		},
		status=status.HTTP_400_BAD_REQUEST)
	
	if request.method == 'GET':
		serializer = MakaleSerializer(makale_instance)
		return Response(serializer.data)
	elif request.method == 'PUT':
		serializer = MakaleSerializer(makale_instance, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		else:
			return Response(status=status.HTTP_400_BAD_REQUEST)

	elif request.method == 'DELETE':
		makale_instance.delete()
		return Response({
			'işlem':{
				'code': 204,
				'message' : f'({pk}) id numarılı makale başarıyla silindi.'
			}
		},
			status=status.HTTP_204_NO_CONTENT
		)
"""
