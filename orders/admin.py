from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from unfold.admin import ModelAdmin

from orders.models import Order


@admin.register(Order)
class OrderAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ['user', "payment_status", "created_at", "updated_at"]
    search_fields = ['user__mobile_phone', 'course__name']
    raw_id_fields = ['user']
    list_select_related = ['user']
    filter_horizontal = ['course']
    list_filter = ['payment_status', 'created_at', 'updated_at']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        q = qs.prefetch_related('course')
        return q
