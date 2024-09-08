from django.contrib import admin
from courses.models import CourseCategory, Course, Comment
from django.utils.translation import gettext_lazy as _


# Register your models here.
# simple filter in CourseAdmin
class SalesFilter(admin.SimpleListFilter):
    title = 'Sales'

    def lookups(self, request, model_admin):
        return [
            ("0-50", _("Show less than 50 course sold")),
            ("50-100", _("Show less than 100 course sold")),
            ("100-500", _("Show range 100 to 500 course sold")),
            ("500-1000", _("show range 500 to 1000 course sold")),
            ("1000", _("show biggest 1000 course sold"))
        ]

    def queryset(self, request, queryset):
        if self.value() == "0-50":
            return queryset.filter()
        elif self.value() == "50-100":
            return queryset.filter()
        elif self.value() == "100-500":
            return queryset.filter()
        elif self.value() == "500-1000":
            return queryset.filter()
        else:
            return queryset.filter()


@admin.register(CourseCategory)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "user", "price", "final_price", "is_active", "sales", "created_at")
    list_filter = ("created_at", "updated_at", "is_active")
    list_max_show_all = 20
    list_editable = ("is_active",)
    date_hierarchy = "created_at"
    search_fields = ("name", "user__mobile_phone")
    prepopulated_fields = {"slug": ("name",)}
    list_select_related = ("user", "category")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "public", "created_at")
    list_editable = ("public", )
    list_max_show_all = 30
    search_fields = ("user__mobile_phone", "course__name")
    list_filter = ("created_at", "updated_at")
    date_hierarchy = "created_at"
    list_select_related = ("user", "course")
