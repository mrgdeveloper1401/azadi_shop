from rest_framework.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, token_verify

from users.views import UserRegistrationAPIView, UserVerifyCodeAPIView


app_name = "users"
urlpatterns = [
    path("register/", UserRegistrationAPIView.as_view(), name="user_register"),
    path("verify_code/", UserVerifyCodeAPIView.as_view(), name="user_verify"),
    # path("login/", UserLoginAPIView.as_view(), name="user_login"),
    # path("logout/", UserLogoutAPIView .as_view(), name="user_logout"),
    # path('password-reset/', UserResetPasswordAPIIView.as_view(), name='password-reset'),
    #  path('password-otp/', PasswordOTPVerificationAPIView.as_view(), name='password-otp'),
    # path('password-reset-confirm/',PasswordResetConfirmAPIView.as_view(), name='password-reset-confirm'),
    path("access_token/", TokenObtainPairView.as_view(), name="user_access_token"),
    path("refresh_token/", TokenRefreshView.as_view(), name="user_refresh_token"),
    path('verify_token/', token_verify, name='user_verify_token'),
    # path("contact_us/", Contact_UsAPIView.as_view(), name="user_contact_us"),
]
