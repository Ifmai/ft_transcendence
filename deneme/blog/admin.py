from django.contrib import admin
from .models import Blog, Catagory


class BlogActiveList(admin.ModelAdmin):
	list_display = ("title", "is_home", "is_active", "slug")
	list_editable = ("is_home", "is_active")
	search_fields = ("title", "context")
	readonly_fields = ("slug",) # sadece readonly yapıyor ve admin page de değiştirilmiyor.

class CatagoryDetalist(admin.ModelAdmin):
	list_display = ("name", "slug")
	readonly_fields = ("slug",)

# Register your models here.
admin.site.register(Blog, BlogActiveList)
admin.site.register(Catagory, CatagoryDetalist)