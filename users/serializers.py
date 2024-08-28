from rest_framework import serializers
from users.models import UserAccount,UserInfo,Otp
from django.core.exceptions import ValidationError
import random

from django.contrib.auth import authenticate,logout
from rest_framework.exceptions import AuthenticationFailed
class UserRegisterSerializer(serializers.Serializer):
   
    username= serializers.CharField()
    password=serializers.CharField()
    # class Meta:
    #     model = UserAccount
    #     fields = ('username',)

    def create(self, value):
        if UserAccount.objects.filter(username=value['username'],password=value['password'],is_active=True).exists():
            raise serializers.ValidationError("Username is already taken.")
        elif UserAccount.objects.filter(username=value['username'],password=value['password'],is_active=False).exists():
            UserAccount.objects.filter(username=value['username'],password=value['password'],is_active=False).delete()
            raise serializers.ValidationError("username is entered is not verified try again")     
        user = UserAccount.objects.create(username=value["username"],password=value['password'])
        user.is_active=False
        user.save()
        code=random.randint(100,999)
        otp=Otp.objects.create(user=user,code=code)  
        # self.send_sms(user.username, code)  
        return user
    
    # def send_sms(self, username, code):
    #     # Replace with your Kavehnegar API details
        #   payload = {
        #             'receptor': username,
        #             'message': f'Your verification code is {code}. It is valid for 5 minutes.',
        #             'apikey': settings.KAVEH_NEGAR_API_KEY
        #         }

        #         response = requests.post(
        #             f'https://api.kavenegar.com/v1/{settings.KAVEH_NEGAR_API_KEY}/sms/send.json',
        #             data=payload
        #         )


        
    #     if response.status_code != 200:
    #         raise serializers.ValidationError("Failed to send SMS")



class OTPVerificationSerializer(serializers.Serializer):

    # username=serializers.CharField()
    otp=serializers.CharField()
        
    def validate(self, value):
        
        try:
            # user=UserAccount.objects.get(username=data['username'])
           otp=Otp.objects.get(code=value['otp'])
            # otp = Otp.objects.get(user__username=data['username'])
        except Otp.DoesNotExist:
            raise serializers.ValidationError("OTP code does not exist.")

        if otp.is_expired():
            otp.delete()
            otp.user.delete()
            raise serializers.ValidationError("OTP code has expired.")

        if otp.code != value['otp']:
            raise serializers.ValidationError("Invalid OTP code.")   
        otp.user.is_active=True
        otp.user.save() 
        return value
    


class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()
    def validate(self, data):
        
        

        if not data['username']or not data['password']:
            raise serializers.ValidationError("Both username and password are required.")

        # Authenticate the user
        try:
            user = UserAccount.objects.get(username=data['username'], password=data['password'],is_active=False)
        # user = authenticate(username=data['username'], password=data['password'])
        except UserAccount.DoesNotExist:
            raise serializers.ValidationError("cant login")
        


        # If authentication is successful, return the user
        data['user'] = user
        return data

class LogoutSerializer(serializers.Serializer):
    def validate(self, data):
        request = self.context.get('request')
        if request.user.is_anonymous:
            raise AuthenticationFailed("User is not logged in.")
        
        # Perform logout
        logout(request)
        return data        
       


    
    
class PasswordResetSerializer(serializers.Serializer):
    email=serializers.CharField()
    
    def validate_email(self, value):
        try:
            user = UserAccount.objects.get(email=value)
        except UserAccount.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        return value


class SetNewPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, value):
        if value['new_password'] != value['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return value


class Contact_usSerializer(serializers.Serializer):
    subject=serializers.CharField()
    message=serializers.CharField()

