from rest_framework.routers import DefaultRouter

from .views import AdminHeaderSiteViewSet, HomeSiteViewSet, AdminContactUsViewSet, AdminTopRankStudentViewSet, \
    AdminTopRankProfessorViewSet, AdminNewsLatterViewSet
from ..views import TopRankStudentViewSet

router = DefaultRouter()
router.register('header_sites', AdminHeaderSiteViewSet, basename='header_site')
router.register('home_site', HomeSiteViewSet, basename='home_site')
router.register('contact_us', AdminContactUsViewSet, basename='contact_us')
router.register('top_rank_student', TopRankStudentViewSet, basename='top_rank_student')
router.register('top_rank_professor', AdminTopRankProfessorViewSet, basename='top_rank_professor')
router.register('news_latter', AdminNewsLatterViewSet, basename='news_latter')

app_name = 'main_settings_admin'
urlpatterns = router.urls
