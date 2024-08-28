from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import UserAccount,UserInfo,Otp
# Register your models here.


@admin.register(UserAccount)
class AccountAdmin(UserAdmin):
    model=UserAccount
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )
    list_display=('first_name','last_name','username','is_active')
    list_filter=('username','is_active','date_joined')
    search_fields=('username',)
    list_editable=('is_active',)


@admin.register(UserInfo)
class AccountAdmin(admin.ModelAdmin):
    model=UserInfo
    list_display=('user_id','grade','major')
    list_filter=('grade','major')
    search_fields=('user_id','grade','major')

@admin.register(Otp)
class AccountAdmin(admin.ModelAdmin):
    model=Otp
