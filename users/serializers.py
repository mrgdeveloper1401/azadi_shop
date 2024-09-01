from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now, timedelta

from users.models import UserAccount, Otp
from users.validators import MobileValidator
from users.random_code import generate_random_code


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    user registration serializer
    """
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
        # TODO send sms
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


class UserVerifyRegisterSerializer(serializers.Serializer):
    """
    verify user register with mobile phone
    """
    code = serializers.IntegerField()

    def validate(self, attrs):
        try:
            get_code = Otp.objects.get(code=attrs['code'])
        except Exception as e:
            raise ValidationError({'message': e})

        if get_code.is_expired():
            get_code.delete_if_expired()
            raise ValidationError({'message': _('otp code is expired please resent code')})
        attrs['user'] = get_code
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


class UserResendVerifyRegisterSerializer(serializers.Serializer):
    """
    resend user verification code
    """
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


class SendCodeMobilePhoneSerializer(serializers.Serializer):
    """
    if you want change profile mobile phone , this is serializer enter mobile phone
    """
    mobile_phone = serializers.CharField(validators=[MobileValidator()])

    def validate(self, attrs):
        mobile_phone = attrs.get('mobile_phone')
        if mobile_phone != self.context['request'].mobile_phone:
            raise ValidationError({"message": _('you do not have permission to do this')})
        if Otp.objects.filter(user=self.context['request']).exists():
            raise ValidationError({'message': _('you have already code please try agin 2 minute')})
        return attrs

    def create(self, validated_data):
        return Otp.objects.create(user=self.context['request'])
        # TODO SEND SMS


class VerifyCodeMobilePhoneSerializer(serializers.Serializer):
    """
    verify code for change mobile and change mobile phone
    """
    code = serializers.IntegerField()
    new_phone = serializers.CharField(validators=[MobileValidator()])

    def validate(self, attrs):
        try:
            get_code = Otp.objects.get(code=attrs['code'])
        except Otp.DoesNotExist:
            raise ValidationError({"message": _("otp query code dose not exist")})

        if get_code.is_expired():
            get_code.delete_if_expired()
            raise ValidationError({"message": "code is expired please resent code"})
        if UserAccount.objects.filter(mobile_phone=attrs['new_phone']).exists():
            raise ValidationError({'message': _('this phone number already exists')})
        return attrs

    def create(self, validated_data):
        user = UserAccount.objects.get(mobile_phone=self.context['request'].mobile_phone)
        user.mobile_phone = validated_data['new_phone']
        user.save()
        Otp.objects.get(code=validated_data['code']).delete()
        return {"message": "successfully change mobile phone"}


class ResetPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, min_length=8)
    new_password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise ValidationError({"message": _('password must be same')})
        try:
            validate_password(attrs['new_password'])
        except Exception as e:
            raise ValidationError({"message": e})
        if not self.context['request'].check_password(attrs['old_password']):
            raise ValidationError({"message": _("old password is wrong")})
        return attrs

    def create(self, validated_data):
        del validated_data['confirm_password']
        user = self.context['request']
        user.set_password(validated_data['new_password'])
        user.save()
        return {"message": "successfully reset password"}


class ForgetPasswordSerializer(serializers.Serializer):
    mobile_phone = serializers.CharField(validators=[MobileValidator()])

    def create(self, validated_data):
        if UserAccount.objects.filter(mobile_phone=validated_data['mobile_phone']).exists():
            user = UserAccount.objects.get(mobile_phone=validated_data['mobile_phone'])
            Otp.objects.create(user=user)
            return {"message": "successfully send code for forget password"}
        return {"message": "successfully send code for forget password"}


class ForgetPasswordConfirmSerializer(serializers.Serializer):
    code = serializers.IntegerField()
    new_password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise ValidationError({"message": _("password must be same")})
        try:
            validate_password(attrs['new_password'])
        except Exception as e:
            raise ValidationError({"message": e})
        code = Otp.objects.get(code=attrs['code'])
        if code.is_expired():
            code.delete_if_expired()

        code['user'] = code.user
        return attrs

    def create(self, validated_data):
        del validated_data['confirm_password']
        user = UserAccount.objects.get(mobile_phone=validated_data['user'].mobile_phone)
        user.set_password(validated_data['new_password'])
        user.save()
        return {"message": _("successfully change password")}
