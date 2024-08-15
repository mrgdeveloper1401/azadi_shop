from django.urls import  include, path
from .views import (
    
PaymentListAPIView,
PaymentDetailAPIView

   
)

app_name = "payments"

urlpatterns = [
    path('payments/', PaymentListAPIView.as_view(), name='payment_list'),  
    path('payments/<int:pk>/', PaymentDetailAPIView.as_view(), name='payment-detail'), 
]