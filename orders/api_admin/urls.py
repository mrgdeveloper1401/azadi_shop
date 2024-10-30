from django.urls import include
from rest_framework.urls import path
from rest_framework_nested.routers import DefaultRouter

from orders.api_admin.views import AdminOrderViewSet, AdminOrderItemViewSet

router = DefaultRouter()
router.register('order', AdminOrderViewSet, basename='admin_order')
router.register('order_item', AdminOrderItemViewSet, basename='admin_order_item')

app_name = 'order_admin'
urlpatterns = router.urls
