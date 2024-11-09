from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import RangeDateTimeFilter

from professors.models import Professor


@admin.register(Professor)
class ProfessorAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ['first_name', "last_name", "nation_code", "email", "birth_date", "education_status", "is_active",
                    "created_at", "updated_at"]
    list_editable = ("is_active", "education_status")
    list_per_page = 20
    search_fields = ['nation_code']
    list_filter_submit = True
    list_filter = ('is_active', ('created_at', RangeDateTimeFilter))
    date_hierarchy = "created_at"
    list_display_links = ["first_name", "last_name", "nation_code", "birth_date", "email"]
