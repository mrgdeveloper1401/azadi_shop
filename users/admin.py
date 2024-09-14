from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.admin import SimpleListFilter

from users.models import UserAccount, UserInfo, Otp


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


@admin.register(UserAccount)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("mobile_phone", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_verified",
                    "is_deleted",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined", "deleted_at")}),
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
    list_display = ("id", "mobile_phone", "email", "first_name", "last_name", "is_staff", 'is_superuser', 'is_active',
                    "is_verified", "is_deleted", "deleted_at")
    list_filter = ("is_staff", "is_superuser", "is_active", 'is_verified', "groups")
    search_fields = ("mobile_phone", "first_name", "last_name", "email")
    ordering = ("mobile_phone",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
    readonly_fields = ['deleted_at']
    list_display_links = ['id', "mobile_phone", "email"]


@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ["id", 'user', 'grade', 'major', 'get_active', "get_is_deleted", "get_is_verified", "get_deleted_at"]
    list_select_related = ['user']
    search_fields = ['user__mobile_phone']
    list_max_show_all = 30
    list_filter = [IsActiveUserInfo]


@admin.register(Otp)
class OtpAdmin(admin.ModelAdmin):
    list_display = ['user', 'id', 'code', 'created_at', 'expired_at']
    list_select_related = ['user']
    search_fields = ['user__mobile_phone']
