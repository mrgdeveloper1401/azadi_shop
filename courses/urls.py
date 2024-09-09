from django.urls import path, include
from courses.views import CommentViewSet, CourseViewSet, CategoryViewSet
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

router = DefaultRouter()
router.register('course', CourseViewSet, basename='course')
router.register('category', CategoryViewSet, basename='category')

course_router = NestedDefaultRouter(router, 'course', lookup='course')
course_router.register('comment', CommentViewSet, basename='comment')

app_name = "course"
urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include(course_router.urls)),
    # path("categories/<int:pk>/", CategoryListAPIView.as_view(), name="detail_category"),
    # path('', include(router.urls)),
    # path('', include('courses.admin_api.urls')),
]
