from pip._vendor.requests.models import Response
from rest_framework import status, mixins, permissions, response, views, viewsets, generics

from drf_spectacular.utils import extend_schema

from . import serializers
from users.models import UserInfo, GradeGpa, User, Otp
from .permissions import IsOwnerProfile, NotAuthenticated


class UserRegistrationViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.UserRegisterSerializer
    queryset = User.objects.only("mobile_phone", "password")
    permission_classes = [NotAuthenticated]


class UserLoginByPhoneViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Otp.objects.all()
    serializer_class = serializers.UserLoginByPhoneSerializer
    permission_classes = [NotAuthenticated]


class UserVerifyOtpApiView(views.APIView):
    serializer_class = serializers.VerifyOtpCodeSerializer
    permission_classes = [NotAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        refresh = validated_data['refresh']
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        res = response.Response({'refresh': refresh_token, "access": access_token})
        res.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=True,
            samesite='Lax',
        )
        res.set_cookie(
            key='refresh_token',
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite='Lax',
        )
        return res


class ProfileViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                     mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserInfo.objects.filter(user=self.request.user).defer("is_deleted", "deleted_at").only(
            "id", "first_name", "last_name", "email", "bio", "birth_date", "created_at", "updated_at",
            "user_info_image__image", "user_info_image_id", "user_info_image__height", "user_info_image__width"
        ).select_related("user_info_image")


class LoginByPasswordApiView(views.APIView):
    serializer_class = serializers.UserLoginByPasswordSerializer
    permission_classes = [NotAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        refresh = validated_data['refresh']
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        res = response.Response({'refresh': refresh_token, "access": access_token}, status=status.HTTP_200_OK)
        res.set_cookie("refresh", httponly=True, samesite='Lax', secure=True)
        res.set_cookie("access", httponly=True, samesite='Lax', secure=True)
        return res


class ResetPasswordAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.ResetPasswordSerializer

    def post(self, request):
        ser_data = serializers.ResetPasswordSerializer(data=request.data, context={'request': request.user})
        ser_data.is_valid(raise_exception=True)
        ser_data.save()
        return response.Response({"message": "کاربر گرامی پسورد شما با موفقیت تغییر یافت"}, status=status.HTTP_200_OK)


class ForgetPasswordApiView(views.APIView):
    @extend_schema(
        request=serializers.ForgetPasswordSerializer,
        responses={200: serializers.ForgetPasswordSerializer},
        description="for recovery password, user must be enter mobile phone"
    )
    def post(self, request):
        ser_data = serializers.ForgetPasswordSerializer(data=request.data)
        ser_data.is_valid(raise_exception=True)
        ser_data.save()
        return response.Response({"message": "در صورت وجود حساب یک کد بازیابی ارسال خواهد شد"}, status=status.HTTP_200_OK)


class ForgetPasswordConfirmAPIView(views.APIView):
    @extend_schema(
        request=serializers.ForgetPasswordConfirmSerializer,
        responses={200, serializers.ForgetPasswordConfirmSerializer}
    )
    def post(self, request):
        ser_data = serializers.ForgetPasswordConfirmSerializer(data=request.data)
        ser_data.is_valid(raise_exception=True)
        ser_data.save()
        return response.Response({"message": "کاربر گرامی پسورد شما با موفقیت تغییر یافت"}, status=status.HTTP_200_OK)


class GradeGpaViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                      mixins.UpdateModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.GradeSerializer
    permission_classes = [IsOwnerProfile]

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def get_queryset(self):
        return (GradeGpa.objects.filter(user=self.request.user, user__is_active=True, user__is_verified=True).
                select_related('user', 'grade'))

    def get_serializer_context(self):
        return {'user': self.request.user}


class SendOtpCodeApiView(views.APIView):
    serializer_class = serializers.SendOtpCodeSerializer

    def post(self, request, *args, **kwargs):
        ser_data = serializers.SendOtpCodeSerializer(data=request.data)
        ser_data.is_valid(raise_exception=True)
        ser_data.save()
        return response.Response({"message": "کاربر گرامی کد برای شما ارسال خواهد شد"}, status=status.HTTP_201_CREATED)
