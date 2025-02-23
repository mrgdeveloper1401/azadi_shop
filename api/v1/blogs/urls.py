from django.urls import include
from rest_framework.urls import path
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

from . import views

router = DefaultRouter()

router.register('category', views.CategoryNodeViewSet, basename='category')

router.register('posts', views.PostViewSet, basename='posts')

category = NestedDefaultRouter(router, 'category', lookup='category')

category.register('posts', views.PostViewSet, basename='post')

app_name = "v1_blogs"

urlpatterns = [
    path('', include(router.urls)),
    path('', include(category.urls)),
]
