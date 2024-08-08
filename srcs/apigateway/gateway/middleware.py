import requests
from django.http import JsonResponse
import json
from http.cookies import SimpleCookie

#Request istek 
#Response yanıt



class APIGatewayMiddleware:
	def __init__(self, get_response):
		self.get_response = get_response
	
	def __call__(self, request):
		response = self.process_request(request)
		if response:
			return response
		return self.get_response(request)

	def get_csrf_token_cookie(self, cookie):
		if cookie:
			cookies = SimpleCookie(cookie)
			csrftoken = cookies.get('csrftoken')
			if csrftoken:
				return csrftoken.value
			else:
				return None
		else:
			return None
	
	def process_request(self, request):
		path = request.path
		method = request.method
		print(request.headers)
		cookie = request.headers.get('Cookie')
		headers = {'Content-Type': 'application/json', 'Origin' : 'https://alp.com.tr', 'Referer' : 'https://alp.com.tr/register'}
		body = request.body

		csrftoken = self.get_csrf_token_cookie(cookie)
		#if cookie
		# Burada, path'e göre mikroservise yönlendirme yapıyoruz
		if path.startswith('/api/users/'):
			url = f'http://userservice:8001{path}'
		else:
			return None
		try:
			# if csrftoken is None:
			# 	raise ValueError("Eksik Bilgi Girişi.")
			if method == 'GET':
				response = requests.get(url, headers=headers)
			elif method == 'POST':
				print("post gitti")
				response = requests.post(url, headers=headers, data=body)
			elif method == 'PUT':
				print("put gitti")
				response = requests.put(url, headers=headers, data=body)
			elif method == 'DELETE':
				response = requests.delete(url, headers=headers)
			return JsonResponse(response.json(), status=response.status_code)
		except requests.exceptions.RequestException as e:
			return JsonResponse({'error': str(e)}, status=500)