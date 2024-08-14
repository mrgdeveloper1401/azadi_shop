from django.contrib import admin
from .models import CourseCategory,Course
# Register your models here.
@admin.register(CourseCategory)
class Categoryadmin(admin.ModelAdmin):
    list_display=('name',)
    search_fields=('name',)
    
@admin.register(Course)
class Courseadmin(admin.ModelAdmin):
    list_display=('name','price','category','user')
    search_fields=('name','category','user')
        