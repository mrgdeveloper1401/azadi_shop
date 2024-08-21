from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from .views import (
    
    UserRegisterationAPIView,
    UserVerifyCodeAPIView,
    UserLoginAPIView,
    UserLogoutAPIView,
    UserResetPasswordAPIIView,
    PasswordResetConfirmAPIView,
    Contact_UsAPIView

)
    


app_name = "users"

urlpatterns = [
    path("register/", UserRegisterationAPIView.as_view(), name="user_register"),
    path("verify_code/", UserVerifyCodeAPIView.as_view(), name="user_verify"),
    path("login/", UserLoginAPIView.as_view(), name="user_login"),
    path("logout/", UserLogoutAPIView .as_view(), name="user_logout"),
    path('password-reset/', UserResetPasswordAPIIView.as_view(), name='password-reset'),
    path('password-reset-confirm/<uidb64>/<token>/',PasswordResetConfirmAPIView.as_view(), name='password-reset-confirm'),
    path("access_token/", TokenObtainPairView.as_view(), name="user_access_tooken"),
    path("refresh_token/", TokenRefreshView.as_view(), name="user_refresh_token"),
    path("contact_us/", Contact_UsAPIView.as_view(), name="user_contact_us"),
]






 