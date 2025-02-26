from rest_framework.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# from rest_framework_simplejwt.views import TokenBlacklistView
from rest_framework.routers import DefaultRouter

from . import views

app_name = "users"

router = DefaultRouter()

router.register("register", views.UserRegistrationViewSet, basename="user_register")
router.register("login_by_phone", views.UserLoginByPhoneViewSet, basename="user_login")
router.register("profile", views.ProfileViewSet, basename="user_profile")
# router.register('grade', views.GradeGpaViewSet, basename='grade')

urlpatterns = [
    path("user_otp_verify/", views.UserVerifyOtpApiView.as_view(), name="user_otp_verify"),
    path("login_by_password/", views.LoginByPasswordApiView.as_view(), name="login_by_password"),
    # path("user_verify/", views.UserVerifyRegisterCodeAPIView.as_view(), name="user_verify"),
    # path('reset_password/', views.ResetPasswordAPIView.as_view(), name='reset_password'),
    # path('forget_password/', views.ForgetPasswordApiView.as_view(), name='forget_password'),
    # path('forget_password_confrim/', views.ForgetPasswordConfirmAPIView.as_view(), name='forget_password_confirm'),
    # path("jwt/create/", TokenObtainPairView.as_view(), name="user_access_token"),
    # path("jwt/refresh/", TokenRefreshView.as_view(), name="user_refresh_token"),
    # path('jwt/verify/', token_verify, name='user_verify_token'),
    # path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
    # path('send_otp_code/', views.SendOtpCodeApiView.as_view(), name='send_otp_code'),
    # path('profile/personal-info/', views.ProfileViewSet.as_view(), name='personal-info'),
]
urlpatterns += router.urls
