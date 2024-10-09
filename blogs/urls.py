from django.urls import include
from rest_framework.urls import path
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
# from rest_framework.routers import DefaultRouter

from blogs.views import PostViewSet, CategoryNodeViewSet

router = DefaultRouter()
router.register('category', CategoryNodeViewSet, basename='category')
router.register('posts', PostViewSet, basename='posts')

category = NestedDefaultRouter(router, 'category', lookup='category')
category.register('posts', PostViewSet, basename='post')

app_name = "blogs"
urlpatterns = [
    path('', include(router.urls)),
    path('', include(category.urls)),
]
