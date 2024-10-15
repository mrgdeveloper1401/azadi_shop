from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken


from users.models import UserAccount, Otp, UserInfo, GradeGpa
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
        user = UserAccount.objects.filter(mobile_phone=data['mobile_phone']).last()
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError(_("پسورد ها یکی نیستند"))
        if user and user.is_deleted:
            raise serializers.ValidationError(_("کاربر گرامی شما مسد"))
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
        except Exception as e:
            raise ValidationError({'message': "کد اشتباه هست"})

        if get_code.is_expired():
            get_code.delete_if_expired()
            raise ValidationError({'message': _('کد شما منقضی شده لظفا دوباره درخواست خود را ارسال کنید')})
        if get_code.user.is_active and get_code.user.is_verified:
            get_code.delete()
            raise ValidationError({"message": _("کاربر گرامی شما قبلا حساب خود را تایید کرده اید")})
        attrs['user'] = get_code
        return attrs

    def save(self, **kwargs):
        user = UserAccount.objects.get(mobile_phone=self.validated_data['user'])
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
            # if mobile is existed or not exited we show this message
            # The code will be sent when the mobile number is in our database
            raise ValidationError({'message': _("کاربرگرامی ابتدا باید ثبت نام کنید")})

        if user.is_active and user.is_verified:
            # if mobile is existed or not exited we show this message
            # The code will be sent when the mobile number is in our database
            raise ValidationError({'message': _(f"کاربر گرامی حساب شما از قبل تایید شده هست")})
        if user.is_deleted:
            raise ValidationError({'message': "کاربر گرامی حساب شما مسدود میباشد"})
        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        # TODO send sms
        return Otp.objects.create(user=validated_data['user'], code=generate_random_code())


class SendCodeMobilePhoneSerializer(serializers.Serializer):
    """
    if you want change profile mobile phone , this is serializer enter mobile phone
    """
    mobile_phone = serializers.CharField(validators=[MobileValidator()])

    def validate(self, attrs):
        mobile_phone = attrs.get('mobile_phone')
        if mobile_phone != self.context['request'].mobile_phone:
            raise ValidationError({"message": _('شما مجوز این کار رو ندارید')})
        if Otp.objects.filter(user=self.context['request']).exists():
            raise ValidationError({'message': _('کاربر گرامی شما از قبل یه کد رو دارید لطفا به مدت 2 دقیقه صبر کنید')})
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

    # request_user = serializers.UUIDField(write_only=True)

    def validate(self, attrs):
        try:
            get_code = Otp.objects.get(code=attrs['code'])
        except Otp.DoesNotExist:
            raise ValidationError({"message": _("کد اشتباه هست")})

        if get_code.is_expired():
            get_code.delete_if_expired()
            raise ValidationError(
                {"message": "کاربرا گرامی کد شما منقضی شده هست لطفا دوباره درخواست خود را ارسال کنید"})
        if UserAccount.objects.filter(mobile_phone=attrs['new_phone']).exists():
            raise ValidationError({'message': _('این شماره موبایل از قبل وجود دارد')})
        return attrs

    def create(self, validated_data):
        user = UserAccount.objects.get(mobile_phone=self.context['request'].mobile_phone)
        user.mobile_phone = validated_data['new_phone']
        user.is_verified = False
        user.save()
        Otp.objects.get(code=validated_data['code']).delete()
        return {"message": "کاربر گرامی با موفقیت تلفن شما تغییر کرد"}


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
        return {"message": "کاربر گرامی پسورد شما با موفقیت تغییر پیدا کرد"}


class ForgetPasswordSerializer(serializers.Serializer):
    mobile_phone = serializers.CharField(validators=[MobileValidator()])

    def validate(self, attrs):
        # get user
        user = UserAccount.objects.filter(mobile_phone=attrs['mobile_phone']).last()

        if not UserAccount.objects.filter(mobile_phone=attrs['mobile_phone']).exists():
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
        attrs['user'] = UserAccount.objects.get(mobile_phone=attrs['mobile_phone'])
        return attrs

    def create(self, validated_data):
        try:
            return Otp.objects.create(user=validated_data['user'])
        except UserAccount.DoesNotExist:
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
        model = UserAccount
        fields = ('last_login', "first_name", "last_name", "email", "is_verified", "date_joined", "id")

        extra_kwargs = {
            "last_login": {'read_only': True, "required": False},
            "date_joined": {'read_only': True, "required": False},
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
            UserAccount.objects.get(mobile_phone=attrs['mobile_phone'])
        except Otp.DoesNotExist:
            raise ValidationError({"message": _("کاربر گرامی کد با موفقیت ارسال شد")})
        otp = Otp.objects.filter(user__mobile_phone=attrs['mobile_phone']).last()
        if otp:
            if otp.is_expired():
                otp.delete_if_expired()
            else:
                raise ValidationError({"message": _("کاربر گرامی شما از قبل کد رو ارسال کردید لطفا برای درخواست جدید "
                                                    "2 دقیقه صبر کنید")})
        return attrs

    def save(self, **kwargs):
        user = UserAccount.objects.get(mobile_phone=self.validated_data['mobile_phone'])
        try:
            Otp.objects.get(user__mobile_phone=self.validated_data['mobile_phone'])
        except Otp.DoesNotExist:
            Otp.objects.create(user=user)
