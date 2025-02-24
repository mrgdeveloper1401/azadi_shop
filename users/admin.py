from django.contrib import admin
from django.contrib.auth.forms import AdminUserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.admin import SimpleListFilter
from import_export.admin import ImportExportModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm

from users.models import User, UserInfo, Otp, GradeGpa, Grade, Major

# Register your models here.
admin.site.unregister(Group)


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
class UserAdmin(BaseUserAdmin, ImportExportModelAdmin):
    form = UserChangeForm
    add_form = AdminUserCreationForm
    change_password_form = AdminPasswordChangeForm
    fieldsets = (
        (None, {"fields": ("mobile_phone", "password")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_verified"
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
    list_display = ("id", "mobile_phone", "is_staff", 'is_superuser', 'is_active', "created_at",
                    "updated_at", "is_deleted", "deleted_at")
    list_filter = ("is_staff", "is_superuser", "is_active", "created_at", "updated_at")
    search_fields = ("mobile_phone",)
    ordering = ("-created_at",)
    readonly_fields = ['created_at', "last_login", "updated_at"]
    list_display_links = ['id', "mobile_phone", "created_at", "updated_at"]
    filter_horizontal = []
    list_editable = ['is_staff', "is_superuser", "is_active"]


@admin.register(UserInfo)
class UserInfoAdmin(ImportExportModelAdmin):
    list_display = ["id", 'user', 'email', 'first_name', 'last_name', 'get_active',
                    "created_at", "updated_at", "is_deleted", "deleted_at"]
    list_select_related = ['user']
    search_fields = ["major_major_name", "user__mobile_phone"]
    list_per_page = 100
    list_filter = [IsActiveUserInfo, "created_at", "updated_at"]
    list_display_links = ['id', "user", "email", "first_name", "last_name"]
    raw_id_fields = ['user']
    ordering = ['-created_at']


@admin.register(Otp)
class OtpAdmin(admin.ModelAdmin):
    list_display = ['mobile_phone', 'id', 'code', 'created_at', 'expired_at']
    search_fields = ['mobile_phone']
    list_filter = ["created_at"]


@admin.register(GradeGpa)
class GradeGpaAdmin(ImportExportModelAdmin):
    list_display = ['user', 'id', "grade", "gpa", "created_at", "updated_at"]
    list_select_related = ['user', "grade"]
    search_fields = ['user__mobile_phone']
    list_filter = ['grade', "created_at", "updated_at"]
    raw_id_fields = ['user']
    list_display_links = ['user', "id", "grade", "gpa"]


@admin.register(Grade)
class GradeAdmin(ImportExportModelAdmin):
    pass


@admin.register(Major)
class MajorAdmin(ImportExportModelAdmin):
    pass
