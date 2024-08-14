from django.shortcuts import render
from rest_framework.views import APIView
from .models import Account
from rest_framework.response import Response
from .serializers import UserRegisterSerializer,SendSMSSerializer
from rest_framework import status
# Create your views here.
class UserRegisterationAPIView(APIView):
    message = {'message': 'User created succesfully and send '}
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            #TODO: send sms
        return Response(self.message, status=status.HTTP_200_OK)

class SendSMSAPIView(APIView):
    """
    Check if submitted phone number is a valid phone number and send OTP.
    """


    def post(self, request):
        serializer = SendSMSSerializer(data=request.data)
        if serializer.is_valid():
            # Send OTP
            username=request.data.get('username',None)
            user = Account.objects.filter(username=username,is_verified=False).first()
            user.send_confirmation()

            return Response(status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)