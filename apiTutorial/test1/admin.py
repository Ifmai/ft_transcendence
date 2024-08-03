from django.contrib import admin
from test1.models import Makale, Gazateci
# Register your models here.

class makalelist(admin.ModelAdmin):
	list_display = ("yazar", "baslik", "aktif")
	list_editable = ("aktif",)

admin.site.register(Makale,makalelist)
admin.site.register(Gazateci)
