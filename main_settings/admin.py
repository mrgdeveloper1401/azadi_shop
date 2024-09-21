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
    pass


@admin.register(SiteLogo)
class SiteLogoAdmin(admin.ModelAdmin):
    pass


@admin.register(FooterAddress)
class FooterAddressAdmin(GISModelAdmin):
    pass


@admin.register(FooterSocial)
class FooterSocialAdmin(admin.ModelAdmin):
    pass


@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    pass


@admin.register(Awards)
class AwardsAdmin(admin.ModelAdmin):
    pass


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    pass


@admin.register(SliderProfessorImages)
class ProfessorImagesAdmin(admin.ModelAdmin):
    filter_horizontal = ['professor_image']


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    pass


@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    pass


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ['slider_image']
    list_filter = ['is_active', "created_at", "updated_at"]


@admin.register(TopRankStudent)
class TopRankAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ['is_active', "created_at", "updated_at"]


@admin.register(Footer)
class FooterAdmin(admin.ModelAdmin):
    raw_id_fields = ['footer_logo', "footer_address"]
    inlines = [FooterSocialInline]
    list_filter = ['is_active', "created_at", "updated_at"]
