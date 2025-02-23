from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from unfold.admin import ModelAdmin

from main_settings.models import HeaderSite, Newsletter, ContactUs, HomeSite, TopRankProfessor


# Register your models here.
@admin.register(HeaderSite)
class HeaderSiteAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ['title', "is_active"]
    list_editable = ['is_active']
    list_filter = ['is_active']
    search_fields = ['title']
    list_per_page = 20

    def get_queryset(self, request):
        q = super().get_queryset(request).only("title", "is_active")
        return q


@admin.register(Newsletter)
class NewsletterAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ['email']
    list_per_page = 30
    search_fields = ['email']
    list_filter = ['created_at']
    date_hierarchy = 'created_at'


@admin.register(ContactUs)
class ContactUsAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ['full_name', "mobile_phone"]
    search_fields = ['full_name', "mobile_phone"]
    list_filter = ['created_at']
    date_hierarchy = "created_at"
    list_per_page = 30


@admin.register(HomeSite)
class HomeSiteAdmin(ModelAdmin, ImportExportModelAdmin):
    # filter_horizontal = ['slider_image', "slider_professor_image", "awards_image", "team_image"]
    # list_display = ['header_phone_number', "email", "is_active", "created_at", "updated_at"]
    # list_editable = ['is_active']
    # list_filter = ['created_at', 'updated_at']
    # list_display_links = ['header_phone_number', "email"]
    pass


@admin.register(TopRankProfessor)
class TopRankProfessorAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ['full_name', "field_title"]
    search_fields = ['full_name', "field_title"]
