from django.urls import include
from rest_framework.urls import path
from rest_framework.routers import DefaultRouter

from main_settings.views import (TopRankStudentViewSet, HeaderSiteViewSet, ContactUsViewSet, ServicesViewSet,
                                 NewsLatterViewSet, HomeSiteViewSet)

router = DefaultRouter()
router.register(r'top_rank_student', TopRankStudentViewSet, basename='top_rank_student')
router.register(r'header_site', HeaderSiteViewSet, basename='header_site')
router.register(r'contact_us', ContactUsViewSet, basename="contact_us")
router.register(r'services', ServicesViewSet, basename="services")
router.register(r'news_latter', NewsLatterViewSet, basename='news_latter')
router.register(r'home_site', HomeSiteViewSet, basename='home_site')


app_name = 'main_settings'
urlpatterns = [
    path('', include(router.urls)),
]
