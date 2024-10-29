import requests
from django.http import HttpResponse
from requests.cookies import RequestsCookieJar
import json
from rest_framework.response import Response


class APIGatewayMiddleware:
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		response = self.process_request(request)
		if response:
			return response
		return self.get_response(request)

	def refresh_access_token(self, refresh_token):
		url = 'http://userservice:8001/api/users/token/refresh/'
		payload = {
			'refresh': refresh_token
		}
		try:
			response = requests.post(url, data=payload)
			return response
		except requests.exceptions.RequestException as e:
			return Response({'error: ': e})

	def jwt_token_delete(self, http_response):
		http_response.set_cookie(
			key = 'access_token',
			max_age=0,
			path='/',
			domain=None,
			secure='none',
			expires="Thu, 01 Jan 1970 00:00:00 GMT",
			samesite=None,
		)
		http_response.set_cookie(
			key = 'refresh_token',
			max_age=0,
			path='/',
			domain=None,
			secure='none',
			expires="Thu, 01 Jan 1970 00:00:00 GMT",
			samesite=None,
		)

	def jwt_token_cookies(self, response, http_response):
		try:
			tokens = response.json()
			access_token = tokens.get('access')
			refresh_token = tokens.get('refresh')
			if access_token:
				http_response.set_cookie(
					key='access_token',
					value=access_token,
					httponly=False,
					secure=True,  # HTTPS kullanıyorsanız True yapın
					samesite='Strict',
					max_age=5 * 60,  # 20 saniye
				)
			if refresh_token:
				http_response.set_cookie(
					key='refresh_token',
					value=refresh_token,
					httponly=True,
					secure=True,  # HTTPS kullanıyorsanız True yapın
					samesite='Strict',
					max_age=7 * 24 * 60 * 60,  # 7 gün
				)
			return http_response
		except Exception as e:
			return Response({'error: ': e})

	def process_request(self, request):
		path = request.path
		method = request.method
		headers = dict(request.headers)
		body = request.body
		cookies = request.COOKIES
		cookie_jar = RequestsCookieJar()
		for key, value in cookies.items():
			cookie_jar.set(key, value)

		if path.startswith('/api/users/'):
			url = f'http://userservice:8001{path}'
		elif path.startswith('/api/tournament/'):
			url = f'http://tournament-app:8003{path}'
		try:
			if method == 'GET':
				response = requests.get(url, headers=headers, cookies=cookie_jar)
			elif method == 'POST':
				response = requests.post(url, headers=headers, cookies=cookie_jar, data=body)
			elif method == 'PUT':
				response = requests.put(url, headers=headers, cookies=cookie_jar, data=body)
			elif method == 'DELETE':
				response = requests.delete(url, headers=headers, cookies=cookie_jar)

			#Çalışıyor.
			if response.status_code == 401 and 'refresh_token' in cookies:
				refresh_response = self.refresh_access_token(cookie_jar['refresh_token'])
				if refresh_response.status_code == 200:
					print(f"Bearer {refresh_response.json().get('access')}")
					headers['Authorization'] = f"Bearer {refresh_response.json().get('access')}"
					response = requests.request(method, url, headers=headers, cookies=cookie_jar, data=body)
					http_response = HttpResponse(content=response.content, status=response.status_code, headers=dict(response.headers))
					self.jwt_token_cookies(refresh_response, http_response)
					return http_response

			http_response = HttpResponse(content=response.content, status=response.status_code, headers=dict(response.headers))
			if path == '/api/users/jwtlogin/':
				self.jwt_token_cookies(response, http_response)
			elif path.startswith('/api/users/login42/'):
				self.jwt_token_cookies(response, http_response)
			if path == '/api/users/logout/':
				self.jwt_token_delete(http_response)
			return http_response
		except requests.exceptions.RequestException as e:
			return HttpResponse(json.dumps({'error': str(e)}), status=500, content_type='application/json')
