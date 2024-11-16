from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from unfold.admin import ModelAdmin

from payments.models import Payment


# Register your models here.
@admin.register(Payment)
class PaymentAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ['user', "course", "created_at", "updated_at"]
    list_filter = ['created_at', "updated_at"]
    search_fields = ["course__name"]
    date_hierarchy = 'created_at'
    list_select_related = ['user', "course"]
    list_display_links = ['user', "course"]