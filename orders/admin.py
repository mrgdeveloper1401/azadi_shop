from django.contrib import admin
from django_jalali.admin.filters import JDateFieldListFilter

from orders.models import Cart, CartItem, Order, OrderItem


# Register your models here.
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', "items_number", 'created_at', "updated_at"]
    list_per_page = 20
    list_select_related = ['user']

    def items_number(self, obj):
        return obj.cart_item.count()

    def get_queryset(self, request):
        q = super().get_queryset(request)
        q = q.prefetch_related('cart_item')
        return q


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'course', 'quantity', 'created_at']
    list_filter = [('created_at', JDateFieldListFilter)]
    search_fields = ['course__name']
    list_per_page = 20

    def get_queryset(self, request):
        q = super().get_queryset(request)
        q = q.prefetch_related('cart__user')
        return q


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'payment_status', 'created_at']
    list_filter = ['payment_status', ('created_at', JDateFieldListFilter)]
    list_select_related = ['user']
    search_fields = ['user__mobile_phone']
    list_per_page = 20
    list_display_links = ['id', "user"]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'course', 'order', 'created_at']
    list_filter = [('created_at', JDateFieldListFilter)]
    list_per_page = 20
    search_fields = ['course__name']
    # list_select_related = ['course', 'order']
    list_display_links = ['id', "course"]

    def get_queryset(self, request):
        q = super().get_queryset(request)
        q = q.prefetch_related('course')
        return q
