from django.urls import  include, path
from .views import (
    
   CategoryAPIView,
   CourseAPIView,
   RemainedTimeAPIView,
   DiscountAPIView
   
)

app_name = "courses"

urlpatterns = [
    path("categries/", CategoryAPIView.as_view(), name="category"),
    path("courses/", CourseAPIView.as_view(), name="course"),
    path("discount_courses/",DiscountAPIView.as_view(), name='discount'),
    path("remained_time/",RemainedTimeAPIView.as_view(), name='remained_time')
]