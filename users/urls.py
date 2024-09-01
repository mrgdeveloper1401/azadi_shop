from rest_framework.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, token_verify

from users.views import UserRegistrationAPIView, UserVerifyRegisterCodeAPIView, OtpResendAPIView, SendCodeMobileApiView, \
    VerifyCodeMobileApiview


app_name = "users"
urlpatterns = [
    path("register/", UserRegistrationAPIView.as_view(), name="user_register"),
    path("user_register_verify_code/", UserVerifyRegisterCodeAPIView.as_view(), name="user_verify"),
    path('resend_user_register_otp_code/', OtpResendAPIView.as_view(), name='resend_otp_code'),
    path('send_code_change_mobile/', SendCodeMobileApiView.as_view(), name='send_code'),
    path('verify_code_change_mobile/', VerifyCodeMobileApiview.as_view(), name='verify_code'),
    path("jwt/create/", TokenObtainPairView.as_view(), name="user_access_token"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="user_refresh_token"),
    path('jwt/verify/', token_verify, name='user_verify_token'),
    # path("contact_us/", Contact_UsAPIView.as_view(), name="user_contact_us"),
]
