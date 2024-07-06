from django.db import models

# Create your models here.
class Blog(models.Model):
	title = models.CharField(max_length=100, null=False) # Varsayılan null=False dır True dersek değer tanımlanmak değildir.
	image = models.CharField(max_length=50) #Şuan sadece isim olarak saklıyorum eğitimin ilerisinde öğreticekmiş eğitim seti.
	context = models.TextField(max) # defaul değer 255 dir.
	is_active = models.BooleanField()
	is_home = models.BooleanField(default=False) # bir bilgi kaydedildiğinde default değer false eklenir. veri kaydederken göndermek zorunda kalmayız.


class Catagory(models.Model):
	name = models.CharField(max_length=150)

