from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, CharField
from django.utils.translation import gettext_lazy as _


from users.models import UserAccount, UserInfo, Otp


class AdminUserCreateSerializer(ModelSerializer):
    confirm_password = CharField(write_only=True, min_length=8, style={"input_type": "password"})

    class Meta:
        model = UserAccount
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
        return UserAccount.objects.create_user(**validated_data)


class AdminUserSerializer(ModelSerializer):
    class Meta:
        model = UserAccount
        fields = '__all__'


class AdminUserInfoSerializer(ModelSerializer):
    mobile_phone = CharField(source="user.mobile_phone", read_only=True)

    class Meta:
        model = UserInfo
        fields = '__all__'


class AdminOtpSerializer(ModelSerializer):
    mobile_phone = CharField(source="user.mobile_phone", read_only=True)

    class Meta:
        model = Otp
        fields = '__all__'


class AdminOtpCreateSerializer(ModelSerializer):
    class Meta:
        model = Otp
        fields = ['user']

    def validate(self, attrs):
        user = attrs['user']
        if user.is_active and user.is_verified:
            raise ValidationError({"message": _("account is verify")})
        if user.is_deleted:
            raise ValidationError({"message": _("account is deleted")})
        return attrs

    def create(self, validated_data):
        (code, created) = Otp.objects.get_or_create(**validated_data)
        if code.is_expired:
            code.delete_if_expired()
        return code
