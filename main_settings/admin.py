from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin

from main_settings.models import HeaderSite, SiteLogo, FooterAddress, Footer, FooterSocial, AboutUs, Awards, Newsletter \
    , SliderProfessorImages, ContactUs, Services, Slider, TopRankStudent


# inline
class FooterSocialInline(admin.TabularInline):
    model = FooterSocial
    extra = 1


# Register your models here.
@admin.register(HeaderSite)
class HeaderSiteAdmin(admin.ModelAdmin):
    list_display = ['title', "is_active"]
    list_editable = ['is_active']
    list_filter = ['is_active']
    search_fields = ['title']
    list_per_page = 20


@admin.register(SiteLogo)
class SiteLogoAdmin(admin.ModelAdmin):
    list_display = ['logo', "is_active"]
    list_select_related = ['logo']
    list_editable = ['is_active']
    list_filter = ['is_active']
    list_per_page = 20


@admin.register(FooterAddress)
class FooterAddressAdmin(GISModelAdmin):
    list_display = ['state', "city", "street", "postal_code", "location", "is_active"]
    list_editable = ['is_active']
    list_filter = ['is_active']
    search_fields = ['state', "city", "postal_code"]
    list_per_page = 20


@admin.register(FooterSocial)
class FooterSocialAdmin(admin.ModelAdmin):
    list_display = ['footer', "social_name", "social_url", "is_active"]
    list_editable = ['is_active']
    list_filter = ['is_active']
    search_fields = ['social_name']
    list_per_page = 20


@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ['title', "about_us_image", "is_active"]
    list_editable = ['is_active']
    list_filter = ['is_active', "created_at"]
    search_fields = ['title']
    list_per_page = 20
    list_select_related = ['about_us_image']


@admin.register(Awards)
class AwardsAdmin(admin.ModelAdmin):
    list_display = ['id', "awards_title", "is_active"]
    list_editable = ['is_active']
    list_filter = ['is_active', "created_at", "updated_at"]
    list_per_page = 20
    filter_horizontal = ['awards_image']
    list_display_links = ['id', "awards_title"]
    search_fields = ['awards_title']


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email']
    list_per_page = 30
    search_fields = ['email']
    list_filter = ['created_at']
    date_hierarchy = 'created_at'


@admin.register(SliderProfessorImages)
class ProfessorImagesAdmin(admin.ModelAdmin):
    filter_horizontal = ['professor_image']
    list_filter = ['is_active', "created_at", "updated_at"]
    list_per_page = 20
    date_hierarchy = 'created_at'


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['full_name', "mobile_phone"]
    search_fields = ['full_name', "mobile_phone"]
    list_filter = ['created_at']
    date_hierarchy = "created_at"
    list_per_page = 30


@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    list_display = ['title', "services_image", "is_active"]
    list_editable = ['is_active']
    search_fields = ['title']
    list_per_page = 30
    list_display_links = ['services_image']
    list_filter = ['is_active', "created_at", "updated_at"]


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ['slider_image']
    list_filter = ['is_active', "created_at", "updated_at"]
    search_fields = ['title']
    list_display = ['title', "slug", "is_active"]
    list_editable = ['is_active']


@admin.register(TopRankStudent)
class TopRankAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ['is_active', "created_at", "updated_at"]
    search_fields = ['first_name', "last_name", "fields"]
    list_display = ['first_name', "last_name", "is_active", "fields"]
    list_editable = ['is_active']


@admin.register(Footer)
class FooterAdmin(admin.ModelAdmin):
    raw_id_fields = ['footer_logo', "footer_address"]
    inlines = [FooterSocialInline]
    list_filter = ['is_active', "created_at", "updated_at"]
    list_display = ['footer_logo', "mobile_phone", "email", "is_active"]
    search_fields = ['mobile_phone', "email"]
    list_editable = ['is_active']
