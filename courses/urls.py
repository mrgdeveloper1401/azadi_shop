from django.urls import path
from courses.views import CategoryAPIView, CourseAPIView, RemainedTimeAPIView, DiscountAPIView, CourseCategory
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('comments', CommentViewSet, basename='comment')

app_name = "courses"
urlpatterns = [
    path("", CourseListAPIView.as_view(), name="course"),
    path("update-course/<slug>/", CourseUpdateRetreveDestoryApiView.as_view(), name="update-course"),
    path("categories/", CategoryListAPIView.as_view(), name="category"),
    path("update-category/<int:pk>/", CategoryUpdateRetreveDestoryApiView.as_view(),
                       name="update-category"),
    path('discount/', DiscountCourseApiView.as_view(), name='discount'),
    path('discount/<int:pk>/', DiscountUpdateApiView.as_view(), name='discount-update'),
] + router.urls
