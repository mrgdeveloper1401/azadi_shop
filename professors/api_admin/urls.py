from rest_framework.routers import DefaultRouter

from .views import AdminProfessorViewSet

router = DefaultRouter()
router.register('professor', AdminProfessorViewSet, basename='professor')

app_name = 'professor'
urlpatterns = router.urls
