from django.shortcuts import render
from rest_framework.views import APIView
from .models import UserAccount,UserInfo,MobileCode
from rest_framework.response import Response
from .serializers import UserRegisterSerializer
from rest_framework import status
import random
import requests
from django.conf import settings
from django.core.cache import cache
from django.contrib.auth import authenticate, login,logout
from rest_framework_simplejwt.tokens import RefreshToken


class UserRegisterationAPIView(APIView):
      pass
#     def post(self, request):
#         serializer = UserRegisterSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()

#             #TODO: send sms:

#             to = request.data.get('username',None)
#             code = random.randint(100000, 999999)
#             cache.set(to, code, timeout=90)
#             payload = {
#                 'receptor': to,
#                 'message': f'Your verification code is {code}. It is valid for 5 minutes.',
#                 'apikey': settings.KAVEH_NEGAR_API_KEY
#             }

#             response = requests.post(
#                 f'https://api.kavenegar.com/v1/{settings.KAVEH_NEGAR_API_KEY}/sms/send.json',
#                 data=payload
#             )

#             if response.status_code == 200:
#                 return Response({'status': 'Code sent successfully'}, status=status.HTTP_200_OK)
#             else:
#                 return Response({'error': 'Failed to send SMS'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            

# class UserVerifyCodeAPIView(APIView):

#     def post(self, request):
#         username = request.data.get('username',None)  # The phone number
#         code = request.data.get('code',None)  # The code user submits for verification

#         # Retrieve the code from the cache
#         cached_code = cache.get(username)

#         if cached_code is None:
#             return Response({'error': 'Code has expired'}, status=status.HTTP_400_BAD_REQUEST)

#         if str(cached_code) == str(code):
#             user=Account.objects.get(username=username)
#             user.is_verified=True
#             return Response({'status': 'Code verified successfully'}, status=status.HTTP_200_OK)
#         else:
#             return Response({'error': 'Invalid code'}, status=status.HTTP_400_BAD_REQUEST)


    
# class UserLoginAPIView(APIView):

#     def post(self, request):
#         username = request.data.get('username')
#         password = request.data.get('password')
#         user = authenticate(request, username=username, password=password)
        
#         if user is not None:
#             login(request, user)
#             return Response({'status': 'Login successful'}, status=status.HTTP_200_OK)
#         else:
#             return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


# class UseLogoutAPIView(APIView):
      
#       def post(self, request):
#         logout(request)
#         return Response({'status': 'Logout successful'}, status=status.HTTP_200_OK)
      
#       # Or
      
#       def post(self, request):
#         try:
#             refresh_token = request.data['refresh_token']
#             token = RefreshToken(refresh_token)
#             token.blacklist()
#             return Response(status=status.HTTP_205_RESET_CONTENT)
        
#         except Exception :
#             return Response(status=status.HTTP_400_BAD_REQUEST)


# class UserForgotPasswordAPIIView(APIView):
#     pass    


# class UserContact_UsAPIView(APIView):
#     pass