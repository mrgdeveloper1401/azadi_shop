from django.contrib import admin
from courses.models import CourseCategory, Course
from treebeard.admin import TreeAdmin


# Register your models here.
@admin.register(CourseCategory)
class CategoryAdmin(TreeAdmin):
    pass


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'user')
    search_fields = ('name', 'category', 'user')