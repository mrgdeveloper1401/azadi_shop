from rest_framework import serializers
from users.models import UserAccount,UserInfo,MobileCode
from django.core.exceptions import ValidationError

class UserRegisterSerializer(serializers.ModelSerializer):
   
    username= serializers.JSONField()
    class Meta:
        model = UserAccount
        fields = ('username',)

    # def create(self, validated_data):
    #     if Account.objects.filter(username=validated_data['username']).exists():
    #      raise serializers.ValidationError("Username is already taken.")
    #     user = Account.objects.create(username=validated_data["username"])
    #     user.save()
    #     return user
    
    # def send(self,value):
    #         if  Account.objects.filter(username=value['username'],is_verified=False).exist():
    #            raise serializers.ValidationError("Username is already taken.")
    #         user=Account.objects.filter(username=value['username'],is_verified=False)
    #         user.send_confirmation()
    #         raise serializers.ValidationError('send')
    #         return value 
    
