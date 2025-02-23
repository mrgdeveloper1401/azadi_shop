from django.urls import include
from rest_framework.urls import path
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
# from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('category', views.CategoryNodeViewSet, basename='category')
router.register('posts', views.PostViewSet, basename='posts')
# router.register('last_ten_post', views.ListPostViewSet, basename='last_ten_post')

category = NestedDefaultRouter(router, 'category', lookup='category')
category.register('posts', views.PostViewSet, basename='post')

app_name = "v1_blogs"
urlpatterns = [
    path('', include(router.urls)),
    path('', include(category.urls)),
]
