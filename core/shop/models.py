from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from core.abstract.models import AbstractModelMixin


class Category(MPTTModel):
    name = models.CharField(max_length=256, unique=True, verbose_name="Назва категорії")
    parent = TreeForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="subcategory",
    )
    slug = models.SlugField(max_length=256, verbose_name="Слаг")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")

    class Meta:
        verbose_name = "Категорію"
        verbose_name_plural = "Категорії"

    class MPTTMeta:
        order_insertion_by = ["name"]
        verbose_name = "Категорія"

    def __str__(self):
        return f"{self.name}"
