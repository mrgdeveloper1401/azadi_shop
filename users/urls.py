from django.urls import include, path
from .views import (
    
    UserRegisterationAPIView,
    UserVerifyCodeAPIView,
    UserLoginAPIView,
    UserLogoutAPIView,
    UserForgotPasswordAPIIView,
    UserContact_UsAPIView

)
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
    


app_name = "users"

urlpatterns = [
    path("register/", UserRegisterationAPIView.as_view(), name="user_register"),
    path("verify_code/", UserVerifyCodeAPIView.as_view(), name="user_verify"),
    path("login/", UserLoginAPIView.as_view(), name="user_login"),
    path("logout/", UserLogoutAPIView .as_view(), name="user_logout"),
    path("forgot_password/", UserForgotPasswordAPIIView.as_view(), name="user_forgot_password"),
    path("access_token/", TokenObtainPairView.as_view(), name="user_access_tooken"),
    path("refresh_token/", TokenRefreshView.as_view(), name="user_refresh_token"),
    path("contact_us/", UserContact_UsAPIView.as_view(), name="user_contact_us"),
]





 