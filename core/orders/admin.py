from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    # raw_id_fields = ["book"]
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "first_name",
        "last_name",
        "phone",
        "email",
        "delivery_address",
        "comment",
        "updated",
        "created",
    ]
    readonly_fields = ["created", "updated", "id"]
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "id",
                    "first_name",
                    "last_name",
                    "phone",
                    "email",
                    "delivery_address",
                    "comment",
                ]
            },
        ),
        (
            "Дати",
            {
                "fields": [
                    (
                        "updated",
                        "created",
                    ),
                ]
            },
        ),
    ]
    list_filter = ["updated", "created"]
    inlines = [OrderItemInline]
