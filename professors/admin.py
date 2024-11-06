from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from unfold.admin import ModelAdmin

from professors.models import Professor


@admin.register(Professor)
class ProfessorAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ['first_name', "last_name", "nation_code", "birth_date", "education_status", "is_active",
                    "created_at", "updated_at"]
    list_editable = ("is_active", "education_status")
    list_per_page = 20
    search_fields = ['first_name', 'last_name', 'nation_code']
    list_filter = ['is_active', "created_at", "updated_at"]
    date_hierarchy = "created_at"
    list_display_links = ["first_name", "last_name", "nation_code", "birth_date"]
