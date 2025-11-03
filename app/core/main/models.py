import re

from django.db import models
from ckeditor.fields import RichTextField

from core.orders.validators import PhoneNumberValidator
from core.shop.models import Book


class Email(models.Model):
    email = models.EmailField(verbose_name="Email")
    active = models.BooleanField(default=True, verbose_name="Активний")

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = "Email"
        verbose_name_plural = "Emails"


class Address(models.Model):
    address = models.CharField(max_length=1024, verbose_name="Адреса")
    active = models.BooleanField(default=True, verbose_name="Активний")

    def __str__(self):
        return f"{self.address}"

    class Meta:
        verbose_name = "Адресу"
        verbose_name_plural = "Адреси"


class Phone(models.Model):
    phone = models.CharField(
        max_length=17, verbose_name="Телефон", validators=[PhoneNumberValidator()]
    )
    active = models.BooleanField(default=True, verbose_name="Активний")

    def __str__(self):
        return f"{self.phone}"

    def clean_number(self):
        return re.sub(r"[/(/)/-]", "", self.phone)

    class Meta:
        verbose_name = "Телефон"
        verbose_name_plural = "Телефони"


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


class Document(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    text = RichTextField(verbose_name="Текст")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документи"
        ordering = ["-created"]
