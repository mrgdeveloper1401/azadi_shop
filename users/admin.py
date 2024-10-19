from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.admin import SimpleListFilter
# from django_jalali.admin.filters import JDateFieldListFilter

from users.models import User, UserInfo, Otp, GradeGpa, Grade, Major


# Register your models here.
# user info simple list filter
class IsActiveUserInfo(SimpleListFilter):
    title = _("Is Active User")
    parameter_name = 'is_active'

    def lookups(self, request, model_admin):
        return [
            ('False', _('In active user')),
            ('True', _('Active user')),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'True':
            return queryset.filter(user__is_active=True)
        if self.value() == 'False':
            return queryset.filter(user__is_active=False)
        return queryset


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("mobile_phone", "password")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_verified",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "created_at", "updated_at")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("mobile_phone", "password1", "password2"),
            },
        ),
    )
    list_display = ("id", "mobile_phone", "is_staff", 'is_superuser', 'is_active', "is_verified")
    list_filter = ("is_staff", "is_superuser", "is_active", 'is_verified', "groups", "created_at")
    search_fields = ("mobile_phone",)
    ordering = ("-created_at",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
    readonly_fields = ['created_at', "last_login", "updated_at"]
    list_display_links = ['id', "mobile_phone"]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_super = request.user.is_superuser
        if not is_super:
            form.base_fields['is_superuser'].disabled = True
            form.base_fields['is_deleted'].disabled = True
        return form


@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ["id", 'user', 'grade', 'major', 'email', 'first_name', 'last_name', 'get_active', "get_is_verified"]
    list_select_related = ['user', "grade", "major"]
    search_fields = ["grade__grade_name", "major_major_name", "user__mobile_phone"]
    list_per_page = 100
    list_filter = [IsActiveUserInfo]
    list_display_links = ['id', "user"]
    raw_id_fields = ['user', "grade", "major"]
    ordering = ['-created_at']


@admin.register(Otp)
class OtpAdmin(admin.ModelAdmin):
    list_display = ['mobile_phone', 'id', 'code', 'created_at', 'expired_at']
    search_fields = ['mobile_phone']
    list_filter = ["created_at"]


@admin.register(GradeGpa)
class GradeGpaAdmin(admin.ModelAdmin):
    list_display = ['user', 'id', "grade", "gpa"]
    list_select_related = ['user']
    search_fields = ['user__mobile_phone']
    list_filter = ['grade']
    raw_id_fields = ['user']


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    pass


@admin.register(Major)
class MajorAdmin(admin.ModelAdmin):
    pass
