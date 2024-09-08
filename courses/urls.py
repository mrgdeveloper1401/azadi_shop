from django.urls import path, include
from courses.views import CommentViewSet, CourseViewSet, CategoryListAPIView, DiscountCourseApiView
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

router = DefaultRouter()
router.register('course', CourseViewSet, basename='course')

course_router = NestedDefaultRouter(router, 'course', lookup='course')
course_router.register('comment', CommentViewSet, basename='comment')

app_name = "course"
urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include(course_router.urls)),
    # path("categories/", CategoryListAPIView.as_view(), name="category"),
    # path("categories/<int:pk>/", CategoryListAPIView.as_view(), name="detail_category"),
    # path('discount/', DiscountCourseApiView.as_view(), name='discount'),
    # path('discount/<int:pk>/', DiscountCourseApiView.as_view(), name='detail_discount'),
    # path('', include(router.urls)),
    # path('', include('courses.admin_api.urls')),
]
