from rest_framework.routers import DefaultRouter

from .views import AdminCourseViewSet, AdminCommentViewSet, AdminCategoryViewSet, AdminDiscountCourseViewSet

app_name = 'course_admin'
router = DefaultRouter()
router.register('category', AdminCategoryViewSet, basename='admin_category')
router.register('course', AdminCourseViewSet, basename='admin_course')
router.register('comment', AdminCommentViewSet, basename='admin_comment')
router.register('discount', AdminDiscountCourseViewSet, basename='admin_discount')

urlpatterns = router.urls
