from django.contrib import admin
# from django_jalali.admin.filters import JDateFieldListFilter

from orders.models import Cart, CartItem, Order, OrderItem


# inline
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


# Register your models here.
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', "items_number", "total_price", 'created_at', "updated_at"]
    list_per_page = 20
    search_fields = ['id']
    list_filter = ['created_at', "updated_at"]

    def get_queryset(self, request):
        q = super().get_queryset(request)
        q = q.prefetch_related('cart_item', "cart_item__course__course_discount")
        return q


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'course', 'quantity', "item_price", "calc_final_price", "discount_value", 'created_at']
    list_filter = ['created_at']
    search_fields = ['course__name',]
    list_per_page = 20
    raw_id_fields = ["cart", "course"]
    list_display_links = ['id', "cart"]
    list_select_related = ['cart', "course"]

    def get_queryset(self, request):
        q = super().get_queryset(request)
        q = q.prefetch_related('course__course_discount',)
        return q


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'payment_status', 'order_number', "order_total_price", 'created_at']
    list_filter = ['payment_status', 'created_at']
    search_fields = ['user__mobile_phone', "payment_status", "order_number"]
    list_per_page = 20
    list_display_links = ['id', "user"]
    date_hierarchy = 'created_at'
    readonly_fields = ['order_number']
    raw_id_fields = ['user']

    def get_queryset(self, request):
        q = super().get_queryset(request)
        q = (q.prefetch_related('order_item', "order_item__course", "order_item__course__course_discount").
             select_related('user'))
        return q


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'course', 'order', "course_price", 'created_at']
    list_filter = ['created_at']
    search_fields = ['course__name', "order__user__mobile_phone"]
    list_display_links = ['id', "course"]
    raw_id_fields = ['order', "course"]
    list_per_page = 100
    date_hierarchy = 'created_at'

    def get_queryset(self, request):
        q = super().get_queryset(request)
        q = q.prefetch_related("course__course_discount")
        return q
