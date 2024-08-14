from django.urls import include, path
from .views import (
    
   CategoryAPIView,CourseAPIView
   
)

app_name = "courses"

urlpatterns = [
    path("categries/", CategoryAPIView.as_view(), name="category"),
    path("courses/", CourseAPIView.as_view(), name="course")

   
]