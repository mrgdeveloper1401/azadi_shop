from django.urls import include
from rest_framework.urls import path
from rest_framework_nested.routers import DefaultRouter

from orders.api_admin.views import AdminCartViewSet
router = DefaultRouter()
router.register('admin_order', AdminCartViewSet, basename='admin_order')


app_name = 'admin_order'
urlpatterns = [
    path('', include(router.urls)),
]
