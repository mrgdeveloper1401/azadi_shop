from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken

from images.models import Image
from shop import status_code
from users.models import User, Otp, UserInfo, GradeGpa, Grade
from users.validators import MobileValidator


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    user registration serializer
    """
    confirm_password = serializers.CharField(write_only=True, style={"input_type": "password"})

    class Meta:
        model = User
        fields = ['mobile_phone', "password", "confirm_password"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        del validated_data['confirm_password']
        return User.objects.create(**validated_data)

    def validate(self, attrs):
        mobile_phone = attrs.get('mobile_phone')
        password = attrs.get("password")
        confirm_password = attrs.get('confirm_password')

        get_user = User.objects.filter(mobile_phone=mobile_phone)
        if get_user.exists():
            raise status_code.OBJECT_ALREADY_EXISTS
        if password != confirm_password:
            raise status_code.NOT_EQUAL_FIELD
        return attrs

    def validate_password(self, data):
        try:
            validate_password(data)
        except Exception as e:
            raise e
        return data


class UserLoginByPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Otp
        fields = ['mobile_phone']

    def validate_mobile_phone(self, data):
        get_user = User.objects.filter(mobile_phone=data)
        get_otp_code = Otp.objects.filter(mobile_phone=data)
        if not get_user.exists():
            raise status_code.OBJECT_NOT_FOUND
        if not get_otp_code.last().is_expired():
            raise status_code.WAITING
        return data

    def create(self, validated_data):
        user_ip = self.context['request'].META['REMOTE_ADDR']
        return Otp.objects.create(mobile_phone=validated_data['mobile_phone'], user_ip_address=user_ip)

    def to_representation(self, instance):
        return {'message': _("یک کد تایید برای شما ارسال شد")}


class VerifyOtpCodeSerializer(serializers.Serializer):
    code = serializers.IntegerField()

    def validate(self, attrs):
        user_ip = self.context['request'].META['REMOTE_ADDR']
        get_otp_code = Otp.objects.filter(code=attrs.get('code'), user_ip_address=user_ip)
        if not get_otp_code.exists():
            raise status_code.WRONG_DATA
        if get_otp_code.last().is_expired():
            get_otp_code.delete()
            raise serializers.ValidationError({"message": _("کد شما منقضی شده هست لطفا دوباره درخواست کنید")})
        user = User.objects.filter(mobile_phone=get_otp_code.first().mobile_phone).first()
        refresh = RefreshToken.for_user(user)
        attrs['refresh'] = refresh
        return attrs


class ProfileSerializer(serializers.ModelSerializer):
    user_info_image = serializers.ImageField(required=False)
    user_info_image_url = serializers.SerializerMethodField()

    class Meta:
        model = UserInfo
        exclude = ['is_deleted', "deleted_at", "user"]

    def update(self, instance, validated_data):
        get_user_info_image = validated_data.pop('user_info_image', None)
        if get_user_info_image:
            image = Image.objects.create(image=get_user_info_image)
            instance.user_info_image = image
        for i, j in validated_data.items():
            setattr(instance, i, j)
        instance.save()
        return instance

    def get_user_info_image_url(self, obj):
        return obj.user_info_image_url


class UserLoginByPasswordSerializer(serializers.Serializer):
    mobile_phone = serializers.CharField(validators=[MobileValidator()])
    password = serializers.CharField(write_only=True, min_length=8, style={"input_type": "password"})

    def validate(self, attrs):
        try:
            get_user = User.objects.filter(mobile_phone=attrs['mobile_phone']).last()
        except Exception as e:
            raise status_code.OBJECT_NOT_FOUND
        refresh = RefreshToken.for_user(get_user)
        attrs['refresh'] = refresh
        return attrs


class ForgetPasswordSerializer(serializers.Serializer):
    mobile_phone = serializers.CharField(validators=[MobileValidator()])

    def validate_mobile_phone(self, data):
        get_user = User.objects.filter(mobile_phone=data)
        if not get_user.exists():
            raise status_code.OBJECT_NOT_FOUND
        return data

    def validate(self, attrs):
        user_ip = self.context['request'].META['REMOTE_ADDR']
        get_otp_code = Otp.objects.filter(mobile_phone=attrs['mobile_phone'], user_ip_address=user_ip).last()
        if not get_otp_code.is_expired():
            raise status_code.WAITING
        return attrs

    def create(self, validated_data):
        user_ip = self.context['request'].META['REMOTE_ADDR']
        return Otp.objects.create(mobile_phone=validated_data['mobile_phone'], user_ip_address=user_ip)


class ForgetPasswordConfirmSerializer(serializers.Serializer):
    code = serializers.CharField()
    new_password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)

    def validate_password(self, data):
        try:
            validate_password(data)
        except Exception as e:
            raise e

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"message": _("password must be same")})
        get_user_ip = self.context['request'].META['REMOTE_ADDR']
        get_code = Otp.objects.filter(code=attrs['code'], user_ip_address=get_user_ip)
        if not get_code.exists():
            raise status_code.OBJECT_NOT_FOUND
        if get_code.last().is_expired():
            get_code.delete()
            raise serializers.ValidationError({"message": _("کد شما متقضی شده هست لطفا دوباره درخواست کنید")})
        get_user = User.objects.filter(mobile_phone=get_code.last().mobile_phone)
        attrs['user'] = get_user
        return attrs

    def to_representation(self, instance):
        return {"message": _("پسورد با شما با موفقیت تغییر یافت")}
    
    def save(self, **kwargs):
        valid_data = self.validated_data
        user = valid_data['user'].last()
        user.set_password(valid_data['new_password'])
        user.save()


class ResetPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, min_length=8)
    new_password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, attrs):
        user = self.context['request'].user
        if attrs['new_password'] != attrs['confirm_password']:
            raise ValidationError({"message": _('کاربر گرامی پسورد باید یکی باشد')})
        try:
            validate_password(attrs['new_password'])
        except Exception as e:
            raise e
        if not user.check_password(attrs['old_password']):
            raise ValidationError({"message": _("کاربر گرامی رمز عبور قدیمی شما نامعتبر میباشد")})
        return attrs

    def save(self, **kwargs):
        validate_data = self.validated_data
        del validate_data['confirm_password']
        user = self.context['request'].user
        user.set_password(validate_data['new_password'])
        user.save()

    def to_representation(self, instance):
        return {"message": _("پسورد شما با موفقیت تغییر یافت")}


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
