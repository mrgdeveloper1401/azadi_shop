from django.contrib.auth import login
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenBlacklistView
from rest_framework_simplejwt.serializers import TokenBlacklistSerializer

from users.models import Otp
from users.serializers import UserRegisterSerializer, UserVerifyRegisterSerializer, UserResendVerifyRegisterSerializer, \
    SendCodeMobilePhoneSerializer, VerifyCodeMobilePhoneSerializer, ResetPasswordSerializer, ForgetPasswordSerializer, \
    ForgetPasswordConfirmSerializer
from users.models import UserAccount


class UserRegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserVerifyRegisterCodeAPIView(APIView):
    def post(self, request, *args, **kwargs):
        ser_data = UserVerifyRegisterSerializer(data=request.data)
        ser_data.is_valid(raise_exception=True)
        ser_data.save()
        return Response({"message": 'successfully varify account'}, status=status.HTTP_200_OK)


class OtpResendAPIView(APIView):
    def post(self, request):
        serializer = UserResendVerifyRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': "code is resend"}, status=status.HTTP_201_CREATED)


class SendCodeMobileApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ser_data = SendCodeMobilePhoneSerializer(data=request.data, context={'request': request.user})
        ser_data.is_valid(raise_exception=True)
        ser_data.save()
        return Response({"message": "successfully send code"})


class VerifyCodeMobileApiview(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ser_data = VerifyCodeMobilePhoneSerializer(data=request.data, context={'request': request.user})
        ser_data.is_valid(raise_exception=True)
        ser_data.save()
        return Response({"message": "successfully verify code"}, status=status.HTTP_200_OK)


class ResetPasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ser_data = ResetPasswordSerializer(data=request.data, context={'request': request.user})
        ser_data.is_valid(raise_exception=True)
        ser_data.save()
        return Response({"message": "successfully reset password"}, status=status.HTTP_200_OK)


class ForgetPasswordApiView(APIView):
    def post(self, request):
        ser_data = ForgetPasswordSerializer(data=request.data)
        ser_data.is_valid(raise_exception=True)
        ser_data.save()
        return Response({"message": "we send code and verify for forget password"}, status=status.HTTP_200_OK)


class ForgetPasswordConfirmAPIView(APIView):
    def post(self, request):
        ser_data = ForgetPasswordConfirmSerializer(data=request.data)
        ser_data.is_valid(raise_exception=True)
        ser_data.save()
        return Response({"message": "successfully change password"}, status=status.HTTP_200_OK)
