from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now, timedelta

from users.models import UserAccount, Otp
from users.validators import MobileValidator
from users.random_code import generate_random_code

class UserRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True,
                                             min_length=8,
                                             style={'input_type': 'password'})

    class Meta:
        model = UserAccount
        fields = ('mobile_phone', 'password', 'confirm_password')

        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}}
        }

    def create(self, validated_data):
        del validated_data['confirm_password']
        user = UserAccount.objects.create_user(**validated_data)
        get_code = Otp.objects.get(user__mobile_phone=validated_data['mobile_phone'])
        # send_sms(get_code.user.mobile_phone, get_code.code)
        return user

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError(_("Passwords do not same."))
        try:
            validate_password(data['password'])
        except ValidationError as e:
            return ValidationError({'message': e})
        return data


class OtpVerifySerializer(serializers.Serializer):
    code = serializers.IntegerField()

    def validate(self, attrs):
        try:
            get_code = Otp.objects.get(code=attrs['code'])
            attrs['user'] = get_code
        except Exception as e:
            raise ValidationError({'message': e})
        return attrs

    def save(self, **kwargs):
        user = UserAccount.objects.get(mobile_phone=self.validated_data['user'])
        if not user.is_active and not user.is_verified:
            user.is_active = True
            user.is_verified = True
            user.save()
            Otp.objects.get(code=self.validated_data['code']).delete()
        else:
            Otp.objects.get(code=self.validated_data['code']).delete()
            raise ValidationError(_("You have already verified your account."))


class OtpResendSerializer(serializers.Serializer):
    mobile_phone = serializers.CharField(validators=[MobileValidator()])

    def validate(self, attrs):
        mobile_phone = attrs.get('mobile_phone')

        try:
            user = UserAccount.objects.get(mobile_phone=mobile_phone)
        except UserAccount.DoesNotExist:
            raise ValidationError({'message': _("You must register first.")})

        if user.is_active and user.is_verified:
            raise ValidationError({'message': _("You have already verified your account.")})

        attrs['user'] = user

        if Otp.objects.filter(user=attrs['user']).exists():
            raise ValidationError({"message": _("you have already code, please try 2 minute")})
        return attrs

    def create(self, validated_data):
        # TODO send sms
        return Otp.objects.create(user=validated_data['user'], code=generate_random_code(),
                           expired_at=now() + timedelta(minutes=2))
