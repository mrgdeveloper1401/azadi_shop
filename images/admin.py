from django.contrib import admin

from images.models import Image
# Register your models here.


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ["id", 'title', "file_size"]
    list_display_links = ['id', "title"]
    search_fields = ['title']
    list_per_page = 100
    list_filter = ['created_at', "updated_at"]
