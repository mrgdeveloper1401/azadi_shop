from rest_framework.permissions import BasePermission


class IsAuthenticatedOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        # اجازه ایجاد کامنت به کاربران احراز هویت شده
        if request.method == 'POST':
            return request.user and request.user.is_authenticated

        # برای دیگر روش‌ها (PUT، PATCH، DELETE) باید کاربر مدیر باشد
        return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        # اجازه مشاهده داده‌ها به همه کاربران
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        # اجازه ویرایش یا حذف داده‌ها تنها برای مدیران
        return request.user and request.user.is_staff
