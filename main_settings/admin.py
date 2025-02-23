from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from unfold.admin import ModelAdmin

from main_settings.models import HeaderSite, Newsletter, ContactUs, HomeSite, TopRankProfessor, BusinessAddress, \
    ContactUsSocial


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
    # list_display = ['header_phone_number', "email", "is_active", "created_at", "updated_at"]
    # list_editable = ['is_active']
    # list_filter = ['created_at', 'updated_at']
    # list_display_links = ['header_phone_number', "email"]
    pass


@admin.register(TopRankProfessor)
class TopRankProfessorAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ['full_name', "field_title"]
    search_fields = ['full_name', "field_title"]


@admin.register(BusinessAddress)
class BusinessAddressAdmin(admin.ModelAdmin):
    list_display = ['location_lat', 'location_long', "is_active"]
    list_filter = ['is_active']
    list_per_page = 20


@admin.register(ContactUsSocial)
class ContactUsSocialAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ['social_name', "is_active"]
    list_filter = ['is_active']
