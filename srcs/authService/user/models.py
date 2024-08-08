from django.db import models

from django.contrib.auth.models import User
from PIL import Image

# Create your models here.
class Profil(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil')
	bio = models.CharField(max_length=300, blank=True, null=True)
	city = models.CharField(max_length=120, blank=True, null=True)
	photo = models.ImageField(blank=True, null=True, upload_to='profil_photo/%Y/%m/')
	two_factory = models.BooleanField(default=False)

	class Meta:
		verbose_name_plural = 'Profils'

	def __str__(self):
		return self.user.username
	
	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		if self.photo:
			img = Image.open(self.photo.path)
			if img.height > 600 or img.width > 600:
				output_size = (600,600)
				img.thumbnail(output_size)
				img.save(self.photo.path)


class ProfileComment(models.Model):
	user_profil = models.ForeignKey(Profil, on_delete=models.CASCADE)
	comment_text = models.CharField(max_length=300)
	create_time = models.DateTimeField(auto_now_add=True)
	update_time = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name_plural = 'ProfileCommand'

	def __str__(self):
		return str(self.user_profil.user.username)