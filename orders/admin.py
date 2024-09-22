from django.contrib import admin
from django_jalali.admin.filters import JDateFieldListFilter

from orders.models import Cart, CartItem, Order, OrderItem


# inline
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


# Register your models here.
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', "items_number", "total_price", 'created_at', "updated_at"]
    list_per_page = 20
    list_select_related = ['user']
    raw_id_fields = ['user']
    search_fields = ['id', "user__mobile_phone"]
    list_filter = ['created_at', "updated_at"]

    def get_queryset(self, request):
        q = super().get_queryset(request)
        q = q.prefetch_related('cart_item', "cart_item__course__course_discount")
        return q


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'course', 'quantity', "item_price", 'created_at']
    list_filter = [('created_at', JDateFieldListFilter)]
    search_fields = ['course__name']
    list_per_page = 20
    raw_id_fields = ["cart", "course"]
    list_display_links = ['id', "cart"]
    list_select_related = ['cart', "course"]

    def get_queryset(self, request):
        q = super().get_queryset(request)
        q = q.prefetch_related('course__course_discount', "cart__user")
        return q


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'payment_status', 'created_at']
    list_filter = ['payment_status', ('created_at', JDateFieldListFilter)]
    search_fields = ['user__mobile_phone']
    list_per_page = 20
    list_display_links = ['id', "user"]

    def get_queryset(self, request):
        q = super().get_queryset(request)
        q = q.prefetch_related('order_item').select_related('user')
        return q


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'course', 'order', 'created_at']
    list_filter = [('created_at', JDateFieldListFilter)]
    list_per_page = 20
    search_fields = ['course__name']
    list_display_links = ['id', "course"]

    def get_queryset(self, request):
        q = super().get_queryset(request)
        q = q.prefetch_related('course')
        return q
