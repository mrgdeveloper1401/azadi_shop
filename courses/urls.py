from django.urls import path, include
from courses.views import CommentViewSet, CourseViewSet, CategoryViewSet
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

router = DefaultRouter()
router.register('category', CategoryViewSet, basename='category')
router.register('course', CourseViewSet, basename='course')

category_router = NestedDefaultRouter(router, 'category', lookup='category')
category_router.register('course', CourseViewSet, basename='course')

course_router = NestedDefaultRouter(router, 'course', lookup='course')
course_router.register('comment', CommentViewSet, basename='comment')


app_name = "course"
urlpatterns = [
    path('', include(router.urls)),
    path('', include(category_router.urls)),
    path('', include(course_router.urls)),
]
