from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from blogs.models import CategoryNode, Post


# Register your models here.
@admin.register(CategoryNode)
class CategoryNodeAdmin(TreeAdmin):
    form = movenodeform_factory(CategoryNode)
    prepopulated_fields = {'category_slug': ("category_name",)}
    search_fields = ['category_name']
    list_display = ['category_name', "category_slug"]

# admin.site.register(CategoryNode, CategoryNodeAdmin)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', "post_title", "is_publish", "created_at", "updated_at"]
    list_filter = ['created_at', "updated_at"]
    search_fields = ['title', "author__mobile_phone"]
    date_hierarchy = 'created_at'
    list_select_related = ['author']
    raw_id_fields = ["author"]
    filter_horizontal = ['category']
    prepopulated_fields = {"slug": ("post_title",)}
    list_display_links = ['id', "author"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.prefetch_related('category')
        return qs
