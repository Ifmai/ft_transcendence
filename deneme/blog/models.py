from django.db import models
from django.utils.text import slugify


class Catagory(models.Model):
	name = models.CharField(max_length=150)
	slug = models.SlugField(null=False, blank=True, unique=True, db_index=True, editable=False)

	def __str__(self) -> str:
		return f"{self.name}"
	
	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super().save(*args, **kwargs)


class Blog(models.Model):
	title = models.CharField(max_length=100, null=False) # Varsayılan null=False dır True dersek değer tanımlanmak değildir.
	image = models.ImageField(upload_to="blogs") 
	context = models.TextField(max) # defaul değer 255 dir.
	is_active = models.BooleanField()
	is_home = models.BooleanField(default=False) # bir bilgi kaydedildiğinde default değer false eklenir. veri kaydederken göndermek zorunda kalmayız.
	slug = models.SlugField(null=False, blank=True, unique=True, db_index=True, editable=False)
	catagories = models.ManyToManyField(Catagory, blank=True)
	#catagory_id = models.ForeignKey(Catagory, null=True, default=1, on_delete=models.SET_DEFAULT)
	
	def __str__(self) -> str:
		return f"{self.title}"
	
	def save(self, *args, **kwargs):
		self.slug = slugify(self.title)
		super().save(*args, **kwargs)


