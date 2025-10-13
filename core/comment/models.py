from django.db import models

from core.account.models import User
from core.shop.models import Book


class Comment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Користувавч",
        null=True,
        blank=True,
        default=None,
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Книга",
    )
    body = models.CharField(
        verbose_name="Коментар",
        max_length=1000,
    )
    rating = models.PositiveSmallIntegerField(
        verbose_name="Рейтинг", choices=[(i, str(i)) for i in range(1, 6)]
    )
    name = models.CharField(verbose_name="Ім'я", max_length=255)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")

    class Meta:
        ordering = ["-created"]
        verbose_name = "Коментар"
        verbose_name_plural = "Коментарі"

    def __str__(self):
        return f"{self.id}"
