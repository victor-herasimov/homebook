from django.apps import AppConfig


class OrdersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core.orders"
    label = "core_orders"
    verbose_name = "Закази"
