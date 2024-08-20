from django.contrib import admin
from .models import CourseCategory,Course,DiscountCourse
# Register your models here.
@admin.register(CourseCategory)
class Categoryadmin(admin.ModelAdmin):
    list_display=('name',)
    search_fields=('name',)
    
@admin.register(Course)
class Courseadmin(admin.ModelAdmin):
    list_display=('name','price')
    search_fields=('name',)


@admin.register(DiscountCourse)
class Courseadmin(admin.ModelAdmin):
    list_display=('name','is_active')
    search_fields=('name','is_active')
    list_editable=('is_active',)


 
