from rest_framework.routers import DefaultRouter

from . import views

app_name = "v1_main_settings"

router = DefaultRouter()

router.register(r'header_site', views.HeaderSiteViewSet, basename='header_site')

router.register(r'business_address', views.BusinessAddressViewSet, basename='business_address')

router.register(r'contact_us', views.ContactUsViewSet, basename="contact_us")

router.register(r'news_latter', views.NewsLatterViewSet, basename='news_latter')

router.register(r'home_site', views.HomeSiteViewSet, basename='home_site')

router.register(r'top_rank_professor', views.TopRankProfessorViewSet, basename='top_rank_professor')

router.register(r'social', views.ContactUsSocialViewSet, basename='social')


urlpatterns = router.urls
