from django.db import models


class AbstractMixin:
    slug = models.SlugField(max_length=256, verbose_name="Слсаг")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")


class AbstractModel(AbstractMixin, models.Model):
    class Meta:
        abstract = True
