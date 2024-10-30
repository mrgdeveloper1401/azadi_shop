from rest_framework.routers import DefaultRouter

from .views import AdminImageViewSet

app_name = 'image_admin'
router = DefaultRouter()
router.register('image', AdminImageViewSet, basename='image')

urlpatterns = router.urls
