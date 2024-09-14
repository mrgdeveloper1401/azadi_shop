from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, CharField


from users.models import UserAccount, UserInfo, Otp


class AdminUserCreateSerializer(ModelSerializer):
    confirm_password = CharField(write_only=True, min_length=8)

    class Meta:
        model = UserAccount
        fields = ("mobile_phone", "password", "confirm_password")

        extra_kwargs = {
            "password": {"write_only": True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise ValidationError({"message": "Passwords do not match."})
        try:
            validate_password(attrs['password'])
        except Exception as e:
            raise ValidationError({"message": e})
        return attrs

    def create(self, validated_data):
        del validated_data['confirm_password']
        return UserAccount.objects.create_user(**validated_data)


class AdminUserSerializer(ModelSerializer):
    class Meta:
        model = UserAccount
        fields = '__all__'


class AdminUserInfoSerializer(ModelSerializer):
    class Meta:
        model = UserInfo
        fields = '__all__'


class AdminOtpSerializer(ModelSerializer):
    class Meta:
        model = Otp
        fields = '__all__'
