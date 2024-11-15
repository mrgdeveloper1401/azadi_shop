from rest_framework.urls import path
from rest_framework.routers import DefaultRouter

from .views import OrderViewSet, UserOrderAPIView

app_name = 'orders'
router = DefaultRouter()
router.register('orders', OrderViewSet, basename='order')

urlpatterns = [
    path("user-order/", UserOrderAPIView.as_view(), name="user-order"),
    path('detail-user-order/<int:pk>/', UserOrderAPIView.as_view(), name='detail-user-order'),
]
urlpatterns += router.urls
