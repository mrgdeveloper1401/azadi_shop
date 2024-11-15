from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User, Otp, UserInfo, GradeGpa, Grade
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
        user_account = User.objects.filter(mobile_phone=validated_data['mobile_phone']).last()
        if user_account:
            if user_account.is_deleted:
                raise ValidationError({"message": _("کاربر گرامی دسترسی حساب شما مسدود میباشد!")})
            Otp.objects.get_or_create(mobile_phone=validated_data['mobile_phone'])
            return user_account
        else:
            user, created = User.objects.get_or_create(**validated_data)
            user.set_password(validated_data['password'])
            user.save()
            return user

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError(_("رمز عبور باید یکسان باشد"))
        try:
            validate_password(attrs['password'])
        except ValidationError as e:
            return ValidationError({'message': e})
        try:
            otp = Otp.objects.get(mobile_phone=attrs['mobile_phone'])
        except Otp.DoesNotExist:
            pass
        else:
            if otp:
                if otp.is_expired():
                    otp.delete()
                else:
                    raise ValidationError({"message": _("شما از قبل یه درخواست رو دارید لطفا به مدت 2 دقیقه صبر کنید")})
        return attrs


class UserVerifyRegisterSerializer(serializers.Serializer):
    """
    verify user register with mobile phone
    """
    code = serializers.CharField(max_length=8)

    # mobile_phone = serializers.CharField(required=False, validators=[MobileValidator()])

    def validate(self, attrs):
        try:
            get_code = Otp.objects.get(code=attrs['code'])
        except Exception:
            raise ValidationError({'message': "کد اشتباه هست"})
        else:
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


class ResetPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, min_length=8)
    new_password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, attrs):
        user = self.context['request']
        if attrs['new_password'] != attrs['confirm_password']:
            raise ValidationError({"message": _('کاربر گرامی پسورد باید یکی باشد')})
        try:
            validate_password(attrs['new_password'])
        except Exception as e:
            raise ValidationError({"message": e})
        if not user.check_password(attrs['old_password']):
            raise ValidationError({"message": _("کاربر گرامی رمز عبور قدیمی شما نامعتبر میباشد")})
        return attrs

    def save(self, **kwargs):
        validate_data = self.validated_data
        del validate_data['confirm_password']
        user = self.context['request']
        user.set_password(validate_data['new_password'])
        user.save()


class ForgetPasswordSerializer(serializers.Serializer):
    mobile_phone = serializers.CharField(validators=[MobileValidator()])

    def validate(self, attrs):
        try:
            user = User.objects.get(mobile_phone=attrs['mobile_phone'])
        except User.DoesNotExist:
            raise ValidationError({"message": _("در صورت وجود حساب یک کد بازیابی ارسال خواهد شد")})
        else:
            if user.is_deleted:
                raise ValidationError({"message": _("کاربر گرامی حساب شما مسدود میباشد")})
            if not user.is_active or not user.is_verified:
                raise ValidationError({"message": _("کاربر گرامی ابتدا باید حساب خود را تایید و فعال نمایید")})
        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        try:
            otp = Otp.objects.get(mobile_phone=validated_data['mobile_phone'])
        except Otp.DoesNotExist:
            pass
        else:
            if otp:
                if otp.is_expired():
                    otp.delete()
                else:
                    raise ValidationError({"message": _("شما از قبل یه درخواست رو داشته اید"
                                                        " لطفا به مدت 2 دقیقه صبر کنید")})
        return Otp.objects.create(mobile_phone=validated_data['mobile_phone'])


class ForgetPasswordConfirmSerializer(serializers.Serializer):
    code = serializers.CharField()
    new_password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)

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
        else:
            if code.is_expired():
                code.delete_if_expired()
                raise ValidationError({"message": _("کاربر گرامی این کد منقضی شده هست لطفا دوباره درخواست خود را ارسال "
                                                    "نمایید")})
            user = User.objects.get(mobile_phone=code.mobile_phone)
        attrs['user'] = user
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
    user = serializers.CharField(read_only=True)

    class Meta:
        model = UserInfo
        fields = ("user", "first_name", "last_name", "email")


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['mobile_phone']


class SimpleGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ['grade_name']


class GradeSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)
    # grade = SimpleGradeSerializer()
    grade_name = serializers.SerializerMethodField()

    class Meta:
        model = GradeGpa
        fields = ['id', 'user', 'grade', 'grade_name', "gpa"]
        extra_kwargs = {
            "user": {'read_only': True},
        }

    def get_grade_name(self, obj):
        return obj.grade.grade_name

    def create(self, validated_data):
        grade = validated_data['grade']
        user = self.context['user']
        if GradeGpa.objects.filter(user=user, grade=grade).exists():
            raise ValidationError({"detail": _("شما از قبل چنین پایه رو اضافه کردید")})
        return GradeGpa.objects.create(**validated_data)


class SendOtpCodeSerializer(serializers.Serializer):
    mobile_phone = serializers.CharField(validators=[MobileValidator()])

    # request_user = serializers.UUIDField(read_only=True)

    def validate(self, attrs):
        try:
            user = User.objects.get(mobile_phone=attrs['mobile_phone'])
        except User.DoesNotExist:
            raise ValidationError({"message": _("شما ابتدا باید ثبت نام کنید")})
        else:
            if user.is_deleted:
                raise ValidationError({"message": _("کاربر گرامی دسترسی حساب شما مسدود میباشد")})
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
