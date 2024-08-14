from django.urls import include, path
from .views import (
    
    UserRegisterationAPIView,
    SendSMSAPIView
   
)

app_name = "users"

urlpatterns = [
    path("register/", UserRegisterationAPIView.as_view(), name="user_register"),
    # path("login/", UserLoginAPIView.as_view(), name="user_login"),
    path("send-sms/", SendSMSAPIView.as_view(), name="send_sms"),
    # path(
    #     "verify-phone/", VerifyPhoneNumberAPIView.as_view(), name="verify_phone_number"
    # ),
    # path("", UserAPIView.as_view(), name="user_detail"),
    # path("profile/", ProfileAPIView.as_view(), name="profile_detail"),
    # path("profile/address/", include(router.urls)),
]