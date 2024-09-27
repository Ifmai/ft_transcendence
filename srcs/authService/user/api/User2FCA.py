from user.api.serializers import Profile2FCASerializer, ProfilSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from qrcode.image.svg import SvgImage
from rest_framework import generics
from rest_framework import status
from user.models import Profil
import qrcode.constants
import qrcode
import pyotp
import io


class Enabled2FCA(generics.UpdateAPIView):
	serializer_class = ProfilSerializer
	permission_classes = [IsAuthenticated]

	def get_object(self):
		return Profil.objects.get(user=self.request.user)

	def check_2FCA(self,request,*args,**kwargs):
		code = self.request.data.get('code')
		instance = self.get_object()
		userSecretKey = instance.otp_secret_key
		totp = pyotp.TOTP(userSecretKey)
		totp.now()
		if totp.verify(code) == True:
			instance.two_factory = True
			instance.save()
			return Response({'Success'}, status=status.HTTP_200_OK)
		else:
			return Response({'Again'}, status=status.HTTP_400_BAD_REQUEST)

	def enable_2FCA(self,request, *args, **kwargs):
		instance = self.get_object()
		secret_key = pyotp.random_base32()
		totp = pyotp.TOTP(secret_key)
		uri = totp.provisioning_uri(name=instance.user.email, issuer_name='LastDance')
		qr = qrcode.QRCode(
			version=1,
			error_correction=qrcode.constants.ERROR_CORRECT_L,
			box_size=10,
			border=4,
		)
		qr.add_data(uri)
		qr.make(fit=True)
		svg_buffer= io.BytesIO()
		qr.make_image(image_factory=SvgImage).save(svg_buffer)
		svg_content = svg_buffer.getvalue().decode()
		svg_content = svg_content.replace('svg:', '')
		instance.otp_secret_key = secret_key
		instance.two_factory = False
		instance.save()
		return Response({'qr_svg' : svg_content})

	def disable_2FCA(self, request, *args, **kwargs):
		instance = self.get_object()
		instance.otp_secret_key = ""
		instance.two_factory = False
		instance.save()
		return Response({"Disabled 2FCA."}, status=status.HTTP_200_OK)
	
	def put(self, request, *args, **kwargs):
		select_action = request.data.get('action')
		if select_action == "enable":
			return self.enable_2FCA(self,request, args, kwargs)
		if select_action == "check":
			return self.check_2FCA(self,request, args, kwargs)
		elif select_action == 'disable':
			return self.disable_2FCA(self,request, args, kwargs)
		