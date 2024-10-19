from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from drf_spectacular.utils import extend_schema
from django.utils.timezone import now

from users.serializers import UserRegisterSerializer, UserVerifyRegisterSerializer, ResetPasswordSerializer, \
    ForgetPasswordSerializer, ForgetPasswordConfirmSerializer, ProfileSerializer, SendOtpCodeSerializer, \
    GradeSerializer
from users.models import UserInfo, GradeGpa
from users.permissions import IsOwnerProfile


class UserRegistrationAPIView(APIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserVerifyRegisterCodeAPIView(APIView):
    serializer_class = UserVerifyRegisterSerializer

    def post(self, request, *args, **kwargs):
        ser_data = UserVerifyRegisterSerializer(data=request.data)
        ser_data.is_valid(raise_exception=True)

        tokens = ser_data.save()

        return Response({
            "message": 'کاربر گرامی حساب شما با موفقیت احراز هویت شدید',
            "access_token": tokens['access'],
            "refresh_token": tokens['refresh']
        }, status=status.HTTP_200_OK)


class ResetPasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        ser_data = ResetPasswordSerializer(data=request.data, context={'request': request.user})
        ser_data.is_valid(raise_exception=True)
        ser_data.save()
        return Response({"message": "کاربر گرامی پسورد شما با موفقیت تغییر یافت"}, status=status.HTTP_200_OK)


class ForgetPasswordApiView(APIView):
    @extend_schema(
        request=ForgetPasswordSerializer,
        responses={200: ForgetPasswordSerializer},
        description="for recovery password, user must be enter mobile phone"
    )
    def post(self, request):
        ser_data = ForgetPasswordSerializer(data=request.data)
        ser_data.is_valid(raise_exception=True)
        ser_data.save()
        return Response({"message": "کاربر گرامی ما یک کدی برای شما ارسال کریده ایم"}, status=status.HTTP_200_OK)


class ForgetPasswordConfirmAPIView(APIView):
    @extend_schema(
        request=ForgetPasswordConfirmSerializer,
        responses={200, ForgetPasswordConfirmSerializer}
    )
    def post(self, request):
        ser_data = ForgetPasswordConfirmSerializer(data=request.data)
        ser_data.is_valid(raise_exception=True)
        ser_data.save()
        return Response({"message": "کاربر گرامی پسورد شما با موفقیت تغییر یافت"}, status=status.HTTP_200_OK)


class ProfileViewSet(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = UserInfo.objects.select_related('user').filter(user__is_active=True, user__is_verified=True)
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerProfile]

    def destroy(self, request, *args, **kwargs):
        user_info = self.get_object()
        user = user_info.user
        user.is_active = False
        user.is_verified = False
        user.is_deleted = True
        user.deleted_at = now()
        user.save()
        return super().destroy(request, *args, **kwargs)


class GradeGpaViewSet(RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = GradeGpa.objects.filter(user__is_active=True, user__is_verified=True)
    serializer_class = GradeSerializer
    permission_classes = [IsOwnerProfile]

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class SendOtpCodeApiView(APIView):
    serializer_class = SendOtpCodeSerializer

    def post(self, request, *args, **kwargs):
        ser_data = SendOtpCodeSerializer(data=request.data)
        ser_data.is_valid(raise_exception=True)
        ser_data.save()
        return Response({"message": "کاربر گرامی کد برای شما ارسال خواهد شد"}, status=status.HTTP_201_CREATED)
