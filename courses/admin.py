from django.contrib import admin
from courses.models import CourseCategory, Course, Comment, DiscountCourse, Like
from django.utils.translation import gettext_lazy as _
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory
# from django_jalali.admin.filters import JDateFieldListFilter


class SalesFilter(admin.SimpleListFilter):
    title = 'sale_number'
    parameter_name = 'sale_number'

    def lookups(self, request, model_admin):
        return [
            ("0-50", _("0-50")),
            ("50-100", _("50-100")),
            ("100-500", _("100-500")),
            ("500-1000", _("500-1000")),
            ("1000", _("biggest 1000"))
        ]

    def queryset(self, request, queryset):
        if self.value() == "0-50":
            return queryset.filter(sale_number__gte=0, sale_number__lt=50)
        elif self.value() == "50-100":
            return queryset.filter(sale_number__gte=50, sale_number__lt=100)
        elif self.value() == "100-500":
            return queryset.filter(sale_number__gte=500, sale_number__lt=500)
        elif self.value() == "500-1000":
            return queryset.filter(sale_number__gte=500, sale_number__lt=1000)
        else:
            return queryset.all()


class RateFilter(admin.SimpleListFilter):
    title = 'Rate'
    parameter_name = 'rate'

    def lookups(self, request, model_admin):
        return [
            ('1', _("1")),
            ('2', _("2")),
            ('3', _("3")),
            ('4', _("4")),
            ('5', _("5")),
        ]

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.filter(rating__exact=1)
        elif self.value() == '2':
            return queryset.filter(rating__exact=2)
        elif self.value() == '3':
            return queryset.filter(rating__exact=3)
        elif self.value() == '4':
            return queryset.filter(rating__exact=4)
        elif self.value() == '5':
            return queryset.filter(rating__exact=5)
        else:
            return queryset.all()


@admin.register(CourseCategory)
class CategoryAdmin(TreeAdmin):
    form = movenodeform_factory(CourseCategory)
    raw_id_fields = ['icon']
    list_display = ['name', "slug"]
    list_per_page = 30
    search_fields = ['name']
    prepopulated_fields = {"slug": ("name",)}
    # list_filter = ['is_public']
    list_select_related = ['icon']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "professor", "price", "calc_final_price", "is_active", "is_free", "is_sale",
                    "sale_number", "created_at", 'updated_at', "total_like", "comment_number")
    list_filter = ("is_active", "is_free", "is_sale", SalesFilter, "created_at", "updated_at")
    list_editable = ("is_active", "total_like", "is_free", "is_sale", "price")
    date_hierarchy = "created_at"
    search_fields = ("name", "professor__first_name", "professor__last_name")
    prepopulated_fields = {"slug": ("name",)}
    list_per_page = 20
    list_display_links = ("id", "name")
    raw_id_fields = ("professor", "image")
    list_select_related = ("professor", "image")
    readonly_fields = ['created_at', "updated_at"]
    filter_horizontal = ('category',)

    def get_queryset(self, request):
        q = super().get_queryset(request)
        q = q.prefetch_related("course_discount", "category", "course_comment")
        return q


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "course", "rating", "public", "created_at")
    list_editable = ("public",)
    search_fields = ("user__mobile_phone", "course__name")
    list_filter = ("created_at", "updated_at", RateFilter)
    date_hierarchy = "created_at"
    list_select_related = ("user", "course")
    raw_id_fields = ['user', "course"]
    list_per_page = 20
    list_display_links = ("id", "user", "course")
    readonly_fields = ['rating']


@admin.register(DiscountCourse)
class DiscountCourseAdmin(admin.ModelAdmin):
    list_display = ("course", "discount_type", "value", "is_active", "expired_date", "created_at")
    list_editable = ("is_active",)
    search_fields = ("course__name", "value")
    list_filter = ("is_active", "created_at", "expired_date")
    date_hierarchy = "created_at"
    raw_id_fields = ("course",)
    list_per_page = 20


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', "course", "created_at", "dislike"]
    list_filter = ['created_at', "dislike"]
    date_hierarchy = "created_at"
    list_per_page = 30
    list_select_related = ("user", "course")
    list_editable = ['dislike']
    raw_id_fields = ['user', "course"]
    search_fields = ['user__mobile_phone', 'course__name']
