from django.contrib import admin
# from django_jalali.admin.filters import JDateFieldListFilter

from professors.models import Professor, ProfessorContact
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


@admin.register(ProfessorContact)
class ProfessorContactAdmin(admin.ModelAdmin):
    list_display = ['contact_name', "contact_url", "is_active"]
    list_filter = ['is_active', "created_at", "updated_at"]
    date_hierarchy = "created_at"

    def get_queryset(self, request):
        q = super().get_queryset(request)
        q = q.prefetch_related('contact')
        return q
