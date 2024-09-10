from django.urls import include
from rest_framework.urls import path
from rest_framework_nested.routers import NestedDefaultRouter, DefaultRouter

from orders.views import CartViewSet, CartItemViewSet, OrderViewSet

router = DefaultRouter()
router.register('cart', CartViewSet)
router.register('order', OrderViewSet)

cart_router = NestedDefaultRouter(router, 'cart', lookup='cart')
cart_router.register('items', CartItemViewSet, basename='items')

app_name = 'orders'
urlpatterns = [
    path('', include(router.urls)),
    path('', include(cart_router.urls))
]