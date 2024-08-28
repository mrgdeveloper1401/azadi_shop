from django.shortcuts import render
from rest_framework.views import APIView
from .models import UserAccount,UserInfo,Otp
from rest_framework.response import Response
from .serializers import UserRegisterSerializer,OTPVerificationSerializer,PasswordResetSerializer,SetNewPasswordSerializer,Contact_usSerializer,LoginSerializer,LogoutSerializer
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

                return Response({'status': 'Code sent successfully'}, status=status.HTTP_200_OK)
            else:    
               return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
            
            
            

class UserVerifyCodeAPIView(APIView):
 def post(self, request, *args, **kwargs):
        serializer = OTPVerificationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            
            # OTP is valid, perform necessary actions (e.g., mark as verified, log in the user, etc.)
            return Response({"detail": "OTP verified successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    
class UserLoginAPIView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)  # This creates the session and logs in the user

        # Return a success response
            return Response({
            'detail': 'Login successful',
            'user_id': user.id,
            'username': user.username}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogoutAPIView(APIView) :
    def post(self, request, *args, **kwargs):
        serializer = LogoutSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        # Return a response indicating success
        return Response({
            'detail': 'Logout successful',
        }, status=status.HTTP_200_OK)




# class UseLogoutAPIView(APIView):
      
#     def post(self, request):
#         logout(request)
#         return Response({'status': 'Logout successful'}, status=status.HTTP_200_OK)
      
      



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
                from_email="kymgly@gmail.com",
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
