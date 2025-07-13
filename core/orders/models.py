from django.db import models

from core.abstract.models import AbstractModel
from core.shop.models import Book


class Order(AbstractModel):
    first_name = models.CharField(max_length=256, verbose_name="Ім'я")
    last_name = models.CharField(max_length=256, verbose_name="Прізвище")
    phone = models.CharField(max_length=20, verbose_name="Ім'я")
    email = models.EmailField(verbose_name="Email")
    delivery_address = models.CharField(max_length=512, verbose_name="Адреса доставки")
    comment = models.TextField(blank=True, null=True, verbose_name="Коментар")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Закази"
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["-created"]),
        ]

    def __str__(self):
        return f"Заказ {self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="items", verbose_name="Заказ"
    )
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="order_items", verbose_name="Книга"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Кількість")

    def __str__(self):
        return f"{self.id}"

    def get_cost(self):
        return self.price * self.quantity
