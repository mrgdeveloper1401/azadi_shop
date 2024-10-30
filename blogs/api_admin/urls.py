from rest_framework.routers import DefaultRouter

from .views import AdminPostBlogViewSet, AdminCategoryBlogViewSet


app_name = 'admin_blog'
router = DefaultRouter()
router.register('post', AdminPostBlogViewSet, basename='admin_post')
router.register('category', AdminCategoryBlogViewSet, basename='admin_category')

urlpatterns = router.urls
