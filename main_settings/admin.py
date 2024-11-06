from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from unfold.admin import ModelAdmin

from main_settings.models import HeaderSite, Newsletter, ContactUs, TopRankStudent, HomeSite, TopRankProfessor


# Register your models here.
@admin.register(HeaderSite)
class HeaderSiteAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ['title', "is_active"]
    list_editable = ['is_active']
    list_filter = ['is_active']
    search_fields = ['title']
    list_per_page = 20


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


# @admin.register(Services)
# class ServicesAdmin(ModelAdmin, ImportExportModelAdmin):
#     list_display = ['title', "services_image", "is_active"]
#     list_editable = ['is_active']
#     search_fields = ['title']
#     list_per_page = 30
#     list_display_links = ['services_image']
#     list_filter = ['is_active', "created_at", "updated_at"]
#     raw_id_fields = ['services_image']


@admin.register(TopRankStudent)
class TopRankAdmin(ModelAdmin, ImportExportModelAdmin):
    list_filter = ['is_active', "created_at", "updated_at"]
    search_fields = ['first_name', "last_name", "fields"]
    list_display = ['first_name', "last_name", "is_active", "fields"]
    list_editable = ['is_active']


@admin.register(HomeSite)
class HomeSiteAdmin(ModelAdmin, ImportExportModelAdmin):
    raw_id_fields = ['slider_image', "about_us_image", "slider_professor_image", "awards_image",
                     "team_image"]


@admin.register(TopRankProfessor)
class TopRankProfessorAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ['full_name', "field_title"]
    search_fields = ['full_name', "field_title"]
