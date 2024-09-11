from django.contrib import admin

from orders.models import Cart, CartItem, Order, OrderItem


# Register your models here.
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at']
    list_per_page = 20


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'course', 'quantity', 'created_at']
    list_filter = ['created_at']
    search_fields = ['course__name']
    list_per_page = 20


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'payment_status', 'created_at']
    list_filter = ['payment_status', 'created_at']
    list_select_related = ['user']
    search_fields = ['user__mobile_phone']
    list_per_page = 20
    list_display_links = ['id', "user"]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'course', 'order', 'created_at']
    list_filter = ['created_at']
    list_per_page = 20
    search_fields = ['course__name']
    list_select_related = ['course', 'order']
    list_display_links = ['id', "course"]