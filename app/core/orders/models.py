import re
from django.db import models

from core.abstract.models import AbstractModel
from core.orders.validators import PhoneNumberValidator
from core.shop.models import Book
from core.account.models import User


class Order(AbstractModel):

    class Status(models.TextChoices):
        NEW = ("NEW", "Новий")
        IN_WORK = "IN_WORK", "В роботі"
        SENT = "SENT", "Відправлено"
        DELIVERED = "DELIVERED", "Доставлено"
        CANSELED = "CANSELED", "Відмінено"
        DONE = "DONE", "Виконано"

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None,
        related_name="orders",
        verbose_name="Корисувач",
    )
    status = models.CharField(
        max_length=9, verbose_name="Статус", choices=Status, default=Status.NEW
    )
    first_name = models.CharField(max_length=256, verbose_name="Ім'я")
    last_name = models.CharField(max_length=256, verbose_name="Прізвище")
    phone = models.CharField(
        max_length=20,
        verbose_name="Телефон",
        unique=False,
        validators=[PhoneNumberValidator()],
    )
    email = models.EmailField(verbose_name="Email", unique=False)
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

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def clean_phone_number(self):
        return re.sub(r"[/(/)/-]", "", self.phone)


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

    class Meta:
        verbose_name = "Заказаний товар"
        verbose_name_plural = "Заказані товари"

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.book.price
        return super().save(*args, **kwargs)
