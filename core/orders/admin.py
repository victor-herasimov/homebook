from django.contrib import admin

from .models import Order, OrderItem


@admin.register(OrderItem)
class OrderItemAdin(admin.ModelAdmin):
    def get_cost(self, obj):
        return f"{obj.get_cost()} грн"

    get_cost.short_description = "Сума: "

    verbose_name = "Заказаний товар"
    verbose_name_plural = "Заказані товари"

    fields = ["id", "book", "order", "price", "quantity", "get_cost"]
    list_display = ["id", "book", "order", "price", "quantity"]
    list_filter = ["book", "order"]
    list_display_links = ["id", "book", "order"]
    readonly_fields = ["id", "get_cost"]


class OrderItemInline(admin.TabularInline):
    model = OrderItem

    def get_cost(self, obj):
        if not obj.id is None:
            return f"{obj.get_cost()}"
        else:
            print("Object none")
            return "-"

    get_cost.short_description = "Сума: "

    fields = ["book", "price", "quantity", "get_cost"]
    readonly_fields = ["get_cost"]
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    def get_total_cost(self, obj):
        return obj.get_total_cost()

    get_total_cost.short_description = "Сума: "

    list_display = [
        "id",
        "first_name",
        "last_name",
        "status",
        "phone",
        "email",
        "delivery_address",
        "comment",
        "updated",
        "created",
    ]
    list_display_links = [
        "id",
        "first_name",
        "last_name",
        "phone",
        "email",
    ]
    readonly_fields = ["created", "updated", "id", "get_total_cost"]
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "id",
                    "status",
                    "user",
                    "first_name",
                    "last_name",
                    "phone",
                    "email",
                    "delivery_address",
                    "comment",
                    "get_total_cost",
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
