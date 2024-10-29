from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, CharField
from django.utils.translation import gettext_lazy as _

from users.models import User, UserInfo, Otp, GradeGpa, Major, Grade


class AdminUserCreateSerializer(ModelSerializer):
    confirm_password = CharField(write_only=True, min_length=8, style={"input_type": "password"})

    class Meta:
        model = User
        fields = ("mobile_phone", "password", "confirm_password")

        extra_kwargs = {
            "password": {"write_only": True, "style": {"input_type": "password"}},
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
        return User.objects.create_user(**validated_data)


class AdminUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            "password": {'read_only': True}
        }


class AdminUserInfoSerializer(ModelSerializer):
    mobile_phone = CharField(source="user.mobile_phone", read_only=True)

    class Meta:
        model = UserInfo
        fields = '__all__'


class AdminOtpSerializer(ModelSerializer):
    class Meta:
        model = Otp
        fields = '__all__'
        ordering = ('-created_at',)


class GradeGpaSerializer(ModelSerializer):
    class Meta:
        model = GradeGpa
        fields = '__all__'


class MajorSerializer(ModelSerializer):
    class Meta:
        model = Major
        fields = '__all__'


class GradeSerializer(ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'
