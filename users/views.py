from django.contrib.auth import login
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Otp
from users.serializers import UserRegisterSerializer, OtpVerifySerializer, OtpResendSerializer
from users.models import UserAccount


class UserRegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserVerifyCodeAPIView(APIView):
    def post(self, request, *args, **kwargs):
        ser_data = OtpVerifySerializer(data=request.data)
        ser_data.is_valid(raise_exception=True)
        ser_data.save()
        return Response({"message": 'successfully varify account'}, status=status.HTTP_200_OK)


class OtpResendAPIView(APIView):
    def post(self, request):
        serializer = OtpResendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': "code is resend"}, status=status.HTTP_201_CREATED)
