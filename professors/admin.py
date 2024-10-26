from django.contrib import admin

from professors.models import Professor
# Register your models here.


@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    raw_id_fields = ['certificate', "professor_image"]
    list_display = ['first_name', "last_name", "nation_code", "birth_date", "education_status", "is_active",
                    "created_at"]
    list_editable = ("is_active", )
    list_per_page = 20
    search_fields = ['first_name', 'last_name', 'nation_code']
    list_filter = ['is_active', "created_at", "updated_at"]
    date_hierarchy = "created_at"
    list_display_links = ["first_name", "last_name"]
    list_select_related = ['professor_image']
