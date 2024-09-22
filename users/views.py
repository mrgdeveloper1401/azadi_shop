from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from drf_spectacular.utils import extend_schema

from users.serializers import UserRegisterSerializer, UserVerifyRegisterSerializer, UserResendVerifyRegisterSerializer, \
    SendCodeMobilePhoneSerializer, VerifyCodeMobilePhoneSerializer, ResetPasswordSerializer, ForgetPasswordSerializer, \
    ForgetPasswordConfirmSerializer, ProfileSerializer, SendOtpCodeSerializer
from users.models import UserInfo
from users.permissions import IsOwnerProfile
from core.datetime_config import now


class UserRegistrationAPIView(APIView):
    @extend_schema(
        request=UserRegisterSerializer,
        responses={201: UserRegisterSerializer},
        description="enter mobile phone and password and confirm password for register user,"
                    "one letter password must be upper case"
                    "password must be same"
    )
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserVerifyRegisterCodeAPIView(APIView):
    @extend_schema(
        request=UserVerifyRegisterSerializer,
        responses={201: UserVerifyRegisterSerializer},
        description='enter code and verify user register, but code time more then 2 minute code is expired'
    )
    def post(self, request, *args, **kwargs):
        ser_data = UserVerifyRegisterSerializer(data=request.data)
        ser_data.is_valid(raise_exception=True)
        ser_data.save()
        return Response({"message": 'successfully varify account'}, status=status.HTTP_200_OK)


class OtpResendAPIView(APIView):
    @extend_schema(
        request=UserResendVerifyRegisterSerializer,
        responses={201: UserResendVerifyRegisterSerializer},
        description="resend code to mobile phone for verify user register."
                    "if mobile phone is exited or mobile phone is dose not exited we show massage code is send to "
                    "mobile phone"
    )
    def post(self, request):
        serializer = UserResendVerifyRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': "code is resend"}, status=status.HTTP_201_CREATED)


class SendCodeMobileApiView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=SendCodeMobilePhoneSerializer,
        responses={200: SendCodeMobilePhoneSerializer},
        description='Send confirmation code to change mobile number'
    )
    def post(self, request):
        ser_data = SendCodeMobilePhoneSerializer(data=request.data, context={'request': request.user})
        ser_data.is_valid(raise_exception=True)
        ser_data.save()
        return Response({"message": "successfully send code"})


class VerifyCodeMobileApiview(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=VerifyCodeMobilePhoneSerializer,
        responses={200, VerifyCodeMobilePhoneSerializer},
        description="Verification of the code to change the mobile number"
    )
    def post(self, request):
        ser_data = VerifyCodeMobilePhoneSerializer(data=request.data, context={'request': request.user})
        ser_data.is_valid(raise_exception=True)
        ser_data.save()
        return Response({"message": "successfully verify code"}, status=status.HTTP_200_OK)


class ResetPasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=ResetPasswordSerializer,
        responses={200: ResetPasswordSerializer},
        description="this url for reset password when user is authenticate"
    )
    def post(self, request):
        ser_data = ResetPasswordSerializer(data=request.data, context={'request': request.user})
        ser_data.is_valid(raise_exception=True)
        ser_data.save()
        return Response({"message": "successfully reset password"}, status=status.HTTP_200_OK)


class ForgetPasswordApiView(APIView):
    @extend_schema(
        request=ForgetPasswordSerializer,
        responses={200: ForgetPasswordSerializer},
    )
    def post(self, request):
        ser_data = ForgetPasswordSerializer(data=request.data)
        ser_data.is_valid(raise_exception=True)
        ser_data.save()
        return Response({"message": "we send code and verify for forget password"}, status=status.HTTP_200_OK)


class ForgetPasswordConfirmAPIView(APIView):
    @extend_schema(
        request=ForgetPasswordConfirmSerializer,
        responses={200, ForgetPasswordConfirmSerializer}
    )
    def post(self, request):
        ser_data = ForgetPasswordConfirmSerializer(data=request.data)
        ser_data.is_valid(raise_exception=True)
        ser_data.save()
        return Response({"message": "successfully change password"}, status=status.HTTP_200_OK)


class ProfileViewSet(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = UserInfo.objects.select_related('user').filter(user__is_active=True, user__is_verified=True)
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerProfile]

    def destroy(self, request, *args, **kwargs):
        user_info = self.get_object()
        user = user_info.user
        user.is_active = False
        user.is_verified = False
        user.is_deleted = True
        user.deleted_at = now()
        user.save()
        return super().destroy(request, *args, **kwargs)


class SendOtpCodeApiView(APIView):
    @extend_schema(
        request=SendOtpCodeSerializer,
        responses={201: SendOtpCodeSerializer},
        description='send otp code to mobile phone'
    )
    def post(self, request, *args, **kwargs):
        ser_data = SendOtpCodeSerializer(data=request.data)
        ser_data.is_valid(raise_exception=True)
        ser_data.save()
        return Response({"message": "successfully send otp code"}, status=status.HTTP_201_CREATED)
