from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil')
    bio = models.CharField(max_length=300, blank=True, null=True)
    foto = models.ImageField(blank=True, null=True, upload_to='profil_photo/%Y/%m')

    class Meta:
        verbose_name_plural = 'UserProfile'

    def __str__(self) -> str:
        return self.user.username
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.foto:
            img = Image.open(self.foto.path)
            if img.height > 600 or img.width > 600:
                output_size = (600, 600)
                img.thumbnail(output_size)
                img.save(self.foto.path)
# Create your models here.