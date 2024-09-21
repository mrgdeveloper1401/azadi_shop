from django.urls import include
from rest_framework.urls import path
from rest_framework.routers import DefaultRouter

from main_settings.views import SiteLogoViewSet, SliderProfessorImageViewSet, SliderViewSet, TopRankStudentViewSet, \
    HeaderSiteViewSet, AboutUsViewSet, AwardsViewSet, NewsletterViewSet, FooterViewSet, FooterSocialViewSet, \
    FooterAddressViewSet, ContactUsViewSet, ServicesViewSet

router = DefaultRouter()
router.register(r'site_logo', SiteLogoViewSet, basename='site_logo')
router.register(r'slider_professor_image', SliderProfessorImageViewSet, basename='slider_professor_image')
router.register(r'slider', SliderViewSet, basename='slider')
router.register(r'top_rank_student', TopRankStudentViewSet, basename='top_rank_student')
router.register(r'header_site', HeaderSiteViewSet, basename='header_site')
router.register(r'about_us', AboutUsViewSet, basename='about_us')
router.register(r'awards', AwardsViewSet, basename='awards')
router.register(r'newsletter', NewsletterViewSet, basename='newsletter')
router.register(r'footer', FooterViewSet, basename='footer')
router.register(r'footer_social', FooterSocialViewSet, basename='footer_social')
router.register(r'footer_address', FooterAddressViewSet, basename='footer_address')
router.register(r'contact_us', ContactUsViewSet, basename="contact_us")
router.register(r'services', ServicesViewSet, basename="services")


app_name = 'main_settings'
urlpatterns = [
    path('', include(router.urls)),
]