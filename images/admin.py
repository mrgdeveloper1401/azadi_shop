from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from unfold.admin import ModelAdmin

from images.models import Image
# Register your models here.


@admin.register(Image)
class ImageAdmin(ImportExportModelAdmin):
    list_display = ["id", 'title', "file_size", "created_at"]
    list_display_links = ['id', "title"]
    search_fields = ['title']
    list_per_page = 100
    list_filter = ['created_at', "updated_at"]
