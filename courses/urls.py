from django.urls import path
from courses.views import CourseListAPIView, CategoryListAPIView, DiscountCourseApiView, CommentViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('comments', CommentViewSet, basename='comment')

app_name = "courses"
urlpatterns = [
    path("<slug>", CourseListAPIView.as_view(), name="course"),
    path("categories/<int:pk>/", CategoryListAPIView.as_view(), name="category"),
    path('discount/<int:pk>/', DiscountCourseApiView.as_view(), name='discount'),
] + router.urls
