from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Account
# Register your models here.


@admin.register(Account)
class AccountAdmin(UserAdmin):
    model=Account
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('security_code' ,'is_verified','grade','major')}),
    )
    list_display=('first_name','last_name','username','is_verified')
    list_filter=('username','is_verified','created_at')
    search_fields=('username',)
    ordering=('created_at',)
    list_editable=('is_verified',)
