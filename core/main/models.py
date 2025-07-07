from django.db import models
from ckeditor.fields import RichTextField

from core.shop.models import Book


class Recommendations(models.Model):
    title = models.CharField(max_length=256, verbose_name="Назва")
    image = models.ImageField(
        upload_to="recommendations/", null=True, blank=True, verbose_name="Зображення"
    )
    book = models.OneToOneField(Book, on_delete=models.CASCADE, verbose_name="Книга")
    show = models.BooleanField(default=True, verbose_name="Показувати")

    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Рекомендацію"
        verbose_name_plural = "Рекомендації"
        ordering = ["show", "-created"]


class Info(models.Model):
    text = RichTextField(verbose_name="Текст")

    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")

    class Meta:
        verbose_name = "Інформацію"
        verbose_name_plural = "Інформація"
        ordering = ["-created"]
