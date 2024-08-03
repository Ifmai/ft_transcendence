from django.contrib import admin
from .models import Blog, Catagory
from django.utils.safestring import mark_safe

class BlogActiveList(admin.ModelAdmin):
	list_display = ("title", "is_home", "is_active", "slug", "selected_catagories")
	list_editable = ("is_home", "is_active")
	search_fields = ("title", "context")
	readonly_fields = ("slug",) # sadece readonly yapıyor ve admin page de değiştirilmiyor.
	list_filter = ("catagories", "is_home", "is_active",)

	def selected_catagories(self, obj):
		html = "<ul>"
		for catagory in obj.catagories.all():
			html += "<li>" + catagory.name + "</li>"
		html += "</ul>"
		return mark_safe(html)

""" class CatagoryDetalist(admin.ModelAdmin):
	list_display = ("name", "slug")
	readonly_fields = ("slug",) """

# Register your models here.
admin.site.register(Blog, BlogActiveList)
admin.site.register(Catagory)