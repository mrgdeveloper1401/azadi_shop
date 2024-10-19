from django.urls import include
from rest_framework.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.views import TokenBlacklistView
from rest_framework.routers import DefaultRouter

from users.views import UserRegistrationAPIView, UserVerifyRegisterCodeAPIView, ResetPasswordAPIView,  \
    ForgetPasswordApiView, ForgetPasswordConfirmAPIView, ProfileViewSet, SendOtpCodeApiView, GradeGpaViewSet

app_name = "users"
router = DefaultRouter()
router.register('profile', ProfileViewSet, basename='profile')
router.register('grade', GradeGpaViewSet, basename='grade')

urlpatterns = [
    path("register/", UserRegistrationAPIView.as_view(), name="user_register"),
    path("user_verify/", UserVerifyRegisterCodeAPIView.as_view(), name="user_verify"),
    path('reset_password/', ResetPasswordAPIView.as_view(), name='reset_password'),
    path('forget_password/', ForgetPasswordApiView.as_view(), name='forget_password'),
    path('forget_password_confrim/', ForgetPasswordConfirmAPIView.as_view(), name='forget_password_confirm'),
    path("jwt/create/", TokenObtainPairView.as_view(), name="user_access_token"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="user_refresh_token"),
    # path('jwt/verify/', token_verify, name='user_verify_token'),
    path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('send_otp_code/', SendOtpCodeApiView.as_view(), name='send_otp_code'),
    # path("contact_us/", Contact_UsAPIView.as_view(), name="user_contact_us"),
    # path('delete_otp_code/', schedule_otp, name='delete_otp'),
    path('', include(router.urls)),
]
