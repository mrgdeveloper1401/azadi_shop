from django.shortcuts import render
from rest_framework.views import APIView
from .models import UserAccount,UserInfo,MobileCode
from rest_framework.response import Response
from .serializers import UserRegisterSerializer,PasswordResetSerializer,SetNewPasswordSerializer,Contact_usSerializer
from rest_framework import status
import random
import requests
from django.conf import settings
from django.core.cache import cache
from django.contrib.auth import authenticate, login,logout
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_decode
from django.core.mail import send_mail
from django.utils.encoding import force_bytes

class UserRegisterationAPIView(APIView):
     
        def post(self, request):
            serializer = UserRegisterSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()

            #TODO: send sms:

                to = serializer.validated_data['username']
                code = random.randint(100000, 999999)
                cache.set(to, code, timeout=90)
                payload = {
                    'receptor': to,
                    'message': f'Your verification code is {code}. It is valid for 5 minutes.',
                    'apikey': settings.KAVEH_NEGAR_API_KEY
                }

                response = requests.post(
                    f'https://api.kavenegar.com/v1/{settings.KAVEH_NEGAR_API_KEY}/sms/send.json',
                    data=payload
                )

                if response.status_code == 200:
                    return Response({'status': 'Code sent successfully'}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Failed to send SMS'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            

class UserVerifyCodeAPIView(APIView):

    def post(self, request):
        username = request.data.get('username',None)  # The phone number
        code = request.data.get('code',None)  # The code user submits for verification

        # Retrieve the code from the cache
        cached_code = cache.get(username)

        if cached_code is None:
            return Response({'error': 'Code has expired'}, status=status.HTTP_400_BAD_REQUEST)

        if str(cached_code) == str(code):
            user=UserAccount.objects.get(username=username)
            user.is_verified=True
            return Response({'status': 'Code verified successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid code'}, status=status.HTTP_400_BAD_REQUEST)


    
class UserLoginAPIView(APIView):

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
            
        if not user:
            login(request, user)
            return Response({'status': 'Login successful'}, status=status.HTTP_200_OK)
        else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


class UseLogoutAPIView(APIView):
      
    def post(self, request):
        logout(request)
        return Response({'status': 'Logout successful'}, status=status.HTTP_200_OK)
      
      # Or
      
    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        
        except Exception :
            return Response(status=status.HTTP_400_BAD_REQUEST)



class UserResetPasswordAPIIView(APIView):
    def post(self,request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data['email']
            user = UserAccount.objects.get(email=email)

            # Generate password reset token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = request.build_absolute_uri(f'/password-reset-confirm/?token={token}&uid={uid}')
             # Send email
            send_mail(
                subject="Password Reset Request",
                message=f"Click the link below to reset your password: {reset_url}",
                from_email="noreply@example.com",
                recipient_list=[user.email],
            )
            return Response({"detail": "Password reset email sent."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PasswordResetConfirmAPIView(APIView):
    serializer_class = SetNewPasswordSerializer

    def post(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = UserAccount.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserAccount.DoesNotExist):
            user = None
        
        
        if user and default_token_generator.check_token(user, token):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user.password=serializer.validated_data['new_password']
            user.save()
            return Response({"detail": "Password has been reset."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid token or user ID."}, status=status.HTTP_400_BAD_REQUEST)
       


class Contact_UsAPIView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return Response({"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = Contact_usSerializer(data=request.data)
        if serializer.is_valid():
           
            # Send email
            send_mail(
                subject=serializer.validated_data['subject'],
                message=serializer.validated_data['message'],
                from_email=user.email,
                recipient_list=['admin@example.com'],  
            )
            return Response({"detail": "Message sent successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
