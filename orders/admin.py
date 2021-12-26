from django.contrib import admin
from .models import Order, Payment, OrderProduct


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('payment', 'user', 'product', 'quantity', 'product_price', 'ordered', 'variations')
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'payment', 'order_number', 'created_at', 'updated_at', 'is_ordered')
    readonly_fields = ('user', 'payment', 'order_number', 'is_ordered')
    list_filter = ('is_ordered', 'status',)
    list_per_page = 20
    inlines = [OrderProductInline]


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment_id', 'amount_paid', 'created_at')
    readonly_fields = ('user', 'payment_id', 'amount_paid', 'status', 'payment_method')
    list_per_page = 20


admin.site.register(Order, OrderAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(OrderProduct)

