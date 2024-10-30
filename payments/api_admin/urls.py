from rest_framework.routers import DefaultRouter

from .views import AdminPaymentViewSet

router = DefaultRouter()
router.register(r'payments', AdminPaymentViewSet, basename='admin_payment')

app_name = 'payment_admin'

urlpatterns = router.urls
