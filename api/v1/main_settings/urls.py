from rest_framework.routers import DefaultRouter

from . import views

app_name = "v1_main_settings"

router = DefaultRouter()

router.register(r'header_site', views.HeaderSiteViewSet, basename='header_site')

# router.register(r'top_rank_student', TopRankStudentViewSet, basename='top_rank_student')

router.register(r'contact_us', views.ContactUsViewSet, basename="contact_us")

# router.register(r'services', Se
# rvicesViewSet, basename="services")


router.register(r'news_latter', views.NewsLatterViewSet, basename='news_latter')

router.register(r'home_site', views.HomeSiteViewSet, basename='home_site')

# router.register(r'top_rank_professor', TopRankProfessorViewSet, basename='top_rank_professor')


urlpatterns = router.urls
