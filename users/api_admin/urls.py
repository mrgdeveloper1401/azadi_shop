from django.urls import include
from rest_framework.urls import path
from rest_framework.routers import DefaultRouter

from users.api_admin.views import AdminUserInfoViewSet, AdminOtpViewSet, AdminUserCreateViewSet, GradeViewSet, \
    GradeGpaViewSet, MajorViewSet

router = DefaultRouter()
router.register('user', AdminUserCreateViewSet, basename='create_user')
router.register('otp', AdminOtpViewSet, basename='otp')
router.register('user_info', AdminUserInfoViewSet, basename='user_info')
router.register('grade', GradeViewSet, basename='grade')
router.register('grade_gpa', GradeGpaViewSet, basename='grade_gpa')
router.register('major', MajorViewSet, basename='major')

app_name = 'admin_user'
urlpatterns = [
    path('', include(router.urls)),
]
