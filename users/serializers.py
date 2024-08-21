from rest_framework import serializers
from users.models import UserAccount,UserInfo,MobileCode
from django.core.exceptions import ValidationError

class UserRegisterSerializer(serializers.ModelSerializer):
   
    username= serializers.JSONField()
    class Meta:
        model = UserAccount
        fields = ('username',)

    def create(self, value):
        if UserAccount.objects.filter(username=value['username']).exists():
         raise serializers.ValidationError("Username is already taken.")
        user = UserAccount.objects.create(username=value["username"])
        user.save()
        return value
    
   
    
class PasswordResetSerializer(serializers.Serializer):
     
    email= serializers.JSONField()
    class Meta:
        model = UserAccount
        fields = ('email',)


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
