from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken


from users.models import User, Otp, UserInfo, GradeGpa
from users.validators import MobileValidator


class UserRegisterSerializer(serializers.Serializer):
    """
    user registration serializer
    """
    mobile_phone = serializers.CharField(max_length=11, validators=[MobileValidator()])
    password = serializers.CharField(write_only=True, min_length=8,
                                     style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True,
                                             min_length=8,
                                             style={'input_type': 'password'})

    def create(self, validated_data):
        del validated_data['confirm_password']
        user, created = User.objects.get_or_create(**validated_data)
        return user

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError(_("رمز عبور باید یکسان باشد"))
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

    # request_user = serializers.UUIDField(write_only=True)

    def validate(self, attrs):
        try:
            get_code = Otp.objects.get(code=attrs['code'])
            # get_code = Otp.objects.filter()
        except Exception:
            raise ValidationError({'message': "کد اشتباه هست"})

        if get_code.is_expired():
            get_code.delete_if_expired()
            raise ValidationError({'message': _('کد شما منقضی شده لظفا دوباره درخواست خود را ارسال کنید')})
        attrs['user'] = get_code
        return attrs

    def save(self, **kwargs):
        user = User.objects.get(mobile_phone=self.validated_data['user'])
        if not user.is_active or not user.is_verified:
            user.is_active = True
            user.is_verified = True
            user.save()
            Otp.objects.get(code=self.validated_data['code']).delete()
            refresh = RefreshToken.for_user(user)
            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
        else:
            Otp.objects.get(code=self.validated_data['code']).delete()
            raise ValidationError(_("شما از قبل درخواست رو ارسال کردی لطفا 2 دقیقه صبر کنید"))


class ResetPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, min_length=8)
    new_password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise ValidationError({"message": _('کاربر گرامی پسورد باید یکی باشد')})
        try:
            validate_password(attrs['new_password'])
        except Exception as e:
            raise ValidationError({"message": e})
        if not self.context['request'].check_password(attrs['old_password']):
            raise ValidationError({"message": _("کاربر گرامی رمز عبور قدیمی شما نامعتبر میباشد")})
        return attrs

    def create(self, validated_data):
        del validated_data['confirm_password']
        user = self.context['request']
        user.set_password(validated_data['new_password'])
        user.save()

    def to_representation(self, instance):
        return {"message": _("کاربر گرامی پسورد شما با موفقیت تغییر کرد")}


class ForgetPasswordSerializer(serializers.Serializer):
    mobile_phone = serializers.CharField(validators=[MobileValidator()])

    def validate(self, attrs):
        # get user
        user = User.objects.filter(mobile_phone=attrs['mobile_phone']).last()

        if not User.objects.filter(mobile_phone=attrs['mobile_phone']).exists():
            raise ValidationError({"message": _("کاربر گرامی ما باید ابتدا حساب خود را بسازید")})
        if user.is_deleted:
            raise ValidationError({"message": _("کاربر گرامی حساب شما مسدود میباشد")})
        # if not user.is_active or not user.is_verified:
        if not user.is_active:
            raise ValidationError({"message": _("کاربر گرامی ابتدا باید حساب خود را تایید و فعال نمایید")})
        latest_code = Otp.objects.filter(user__mobile_phone=attrs['mobile_phone']).last()
        if latest_code:
            if latest_code.is_expired():
                latest_code.delete_if_expired()
            else:
                raise ValidationError({"message": _('کاربر گرامی شما از قبل درخواست رو ارسال کردید لطفا به مدت 2 '
                                                    'دقیقه صبر کنید')})
        attrs['user'] = User.objects.get(mobile_phone=attrs['mobile_phone'])
        return attrs

    def create(self, validated_data):
        try:
            return Otp.objects.create(user=validated_data['user'])
        except User.DoesNotExist:
            raise ValidationError({"message": "کاربر گرامی چنین حسابی وجود ندارد"})


class ForgetPasswordConfirmSerializer(serializers.Serializer):
    code = serializers.IntegerField()
    new_password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)

    # request_user = serializers.UUIDField(write_only=True)

    def validate(self, attrs):
        # validate new_password and confirm_password
        if attrs['new_password'] != attrs['confirm_password']:
            raise ValidationError({"message": _("کاربر گرامی پسورد ها باید یکسان باشد")})

        # validate password
        try:
            validate_password(attrs['new_password'])
        except Exception as e:
            raise ValidationError({"message": e})

        # get otp code
        try:
            code = Otp.objects.get(code=attrs['code'])
        except Otp.DoesNotExist:
            raise ValidationError({"message": _("کاربر گرامی کد شما نامعتبر یا صحیح نمیباشد")})

        # validate code is expired
        if code.is_expired():
            code.delete_if_expired()
            raise ValidationError({"message": _("کاربر گرامی این کد منقضی شده هست لطفا دوباره درخواست خود را ارسال "
                                                "نمایید")})

        attrs['user'] = code.user
        return attrs

    def create(self, validated_data):
        del validated_data['confirm_password']
        user = validated_data['user']
        user.set_password(validated_data['new_password'])
        user.save()
        Otp.objects.filter(user=validated_data['user']).delete()
        return {"message": _("کاربر گرامی پسورد شما با موفقیت تغییر پیدا کرد")}


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('last_login', "is_verified", "id")

        extra_kwargs = {
            "last_login": {'read_only': True, "required": False},
            "is_verified": {'read_only': True},
            "id": {'read_only': True},
        }


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserInfo
        fields = ('grade', "major", "user", "gpa")

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user_instance = instance.user
            for key, value in user_data.items():
                setattr(user_instance, key, value)
            user_instance.save()
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradeGpa
        fields = ['id', 'grade', "gpa"]


class SendOtpCodeSerializer(serializers.Serializer):
    mobile_phone = serializers.CharField(validators=[MobileValidator()])

    # request_user = serializers.UUIDField(read_only=True)

    def validate(self, attrs):
        try:
            User.objects.get(mobile_phone=attrs['mobile_phone'])
        except User.DoesNotExist:
            raise ValidationError({"message": _("شما ابتدا باید ثبت نام کنید")})
        otp = Otp.objects.filter(mobile_phone=attrs['mobile_phone']).last()
        if otp:
            if otp.is_expired():
                otp.delete_if_expired()
            else:
                raise ValidationError({"message": _("کاربر گرامی شما از قبل کد رو ارسال کردید لطفا برای درخواست جدید "
                                                    "2 دقیقه صبر کنید")})
        return attrs

    def create(self, validated_data):
        return Otp.objects.get_or_create(**validated_data)
