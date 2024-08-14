from rest_framework import serializers
from users.models import Account,User
from django.core.exceptions import ValidationError

class UserRegisterSerializer(serializers.ModelSerializer):
   
    username= serializers.JSONField()
    class Meta:
        model = Account
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
    
class SendSMSSerializer(serializers.ModelSerializer):
    username= serializers.JSONField()
    class Meta:
        model = Account
        fields = ('username',)
    def validate(self,value) :
        print(value)
        try:
            account=Account.objects.get(username=value['username']) 
            if account.is_verified:
                 raise serializers.ValidationError("Phone number is already verified")
            
        except Account .DoesNotExist:

            raise serializers.ValidationError('This username is not exist')
        return value