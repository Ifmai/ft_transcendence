import qrcode.constants
from rest_framework.permissions import IsAuthenticated
from user.api.serializers import Profile2FCASerializer, ProfilSerializer
from rest_framework.response import Response
from qrcode.image.svg import SvgImage
from rest_framework import generics
from user.models import Profil
import qrcode
import pyotp
import io
#from django.contrib.auth.models import User


class Enabled2FCA(generics.UpdateAPIView):
	serializer_class = ProfilSerializer
	permission_classes = [IsAuthenticated]

	def get_object(self):
		return Profil.objects.get(user=self.request.user)

	def put(self, request, *args, **kwargs):
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
		instance.save()
		return Response({
            'qr_svg': svg_content
        })