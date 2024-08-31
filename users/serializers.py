from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.auth import logout
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from users.models import UserAccount, Otp, PasswordOtp


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
            raise serializers.ValidationError("Passwords do not same.")
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
        user = self.validated_data['user']
        user.is_active = True
        user.is_verified = True
        user.save()
        Otp.objects.get(code=self.validated_data['code']).delete()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):

        if not data['username'] or not data['password']:
            raise serializers.ValidationError("Both username and password are required.")

        # Authenticate the user
        try:
            user = UserAccount.objects.get(username=data['username'], password=data['password'], is_active=False)
        # user = authenticate(username=data['username'], password=data['password'])
        except UserAccount.DoesNotExist:
            raise serializers.ValidationError("cant login")

        # If authentication is successful, return the user
        data['user'] = user
        return data


class LogoutSerializer(serializers.Serializer):
    def validate(self, data):
        request = self.context.get('request')
        if request.user.is_anonymous:
            raise AuthenticationFailed("User is not logged in.")

        # Perform logout
        logout(request)
        return data


class PasswordResetSerializer(serializers.Serializer):
    username = serializers.CharField()

    def create(self, value):
        try:
            user = UserAccount.objects.get(username=value['username'], is_active=True)
            code = random.randint(100, 999)
            otp = PasswordOtp.objects.create(user=user, code=code)
            # self.send_sms(user.username, code)

        except UserAccount.DoesNotExist:
            raise serializers.ValidationError("User with this username does not exist.")
        return value


class PasswordOTPVerificationSerializer(serializers.Serializer):
    # username=serializers.CharField()
    otp = serializers.CharField()

    def validate(self, value):

        try:

            # user=UserAccount.objects.get(username=data['username'])
            otp = PasswordOtp.objects.get(code=value['otp'])
            # otp = Otp.objects.get(user__username=data['username'])
        except PasswordOtp.DoesNotExist:
            raise serializers.ValidationError("OTP code does not exist.")

        if otp.is_expired():
            otp.delete()
            raise serializers.ValidationError("OTP code has expired.")

        if otp.code != value['otp']:
            raise serializers.ValidationError("Invalid OTP code.")
        otp.user.is_verified = True
        return value


class SetNewPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, value):
        if value['new_password'] != value['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        if len(value['confirm_password']) < 8:
            raise serializers.ValidationError("password must be  minimum 8 character")

        return value


class Contact_usSerializer(serializers.Serializer):
    subject = serializers.CharField()
    message = serializers.CharField()
