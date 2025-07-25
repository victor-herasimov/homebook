from decimal import Decimal
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor.fields import RichTextField

from core.abstract.models import AbstractModel


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


class Author(AbstractModel):
    name = models.CharField(max_length=256, verbose_name="Автор")

    class Meta:
        ordering = ["name"]
        verbose_name = "Автора"
        verbose_name_plural = "Автори"

    def __str__(self):
        return f"{self.name}"


class Publisher(AbstractModel):
    name = models.CharField(max_length=256, verbose_name="Видавництво")

    class Meta:
        ordering = ["name"]
        verbose_name = "Видавництво"
        verbose_name_plural = "Видавництва"

    def __str__(self):
        return f"{self.name}"


class Language(AbstractModel):
    language = models.CharField(max_length=100, verbose_name="Мова")

    class Meta:
        ordering = ["language"]
        verbose_name = "Мову"
        verbose_name_plural = "Мови"

    def __str__(self):
        return f"{self.language}"


class Cover(AbstractModel):
    cover = models.CharField(max_length=100, verbose_name="Обкладинка")

    class Meta:
        ordering = ["cover"]
        verbose_name = "Обкладинку"
        verbose_name_plural = "Обкладинки"

    def __str__(self):
        return f"{self.cover}"


class OtherCharacteristicItem(models.Model):
    name = models.CharField(
        max_length=100, verbose_name="Назва додаткової характеристики"
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Назву додаткової характеристики"
        verbose_name_plural = "Назви додаткових характеристик"

    def __str__(self):
        return f"{self.name}"


class OtherCharacteristic(models.Model):
    item = models.ForeignKey(
        OtherCharacteristicItem, on_delete=models.CASCADE, verbose_name="Характеристика"
    )
    value = models.CharField(max_length=64, verbose_name="Значення характеристики")

    class Meta:
        ordering = ["item"]
        verbose_name = "Додаткову характеристика"
        verbose_name_plural = "Додаткові характеристики"
        constraints = [
            models.UniqueConstraint(fields=("item", "value"), name="unique_item_value")
        ]

    def __str__(self):
        return f"{self.item} - {self.value}"


class Book(AbstractModel):
    title = models.CharField(max_length=256, verbose_name="Назва")
    image = models.ImageField(
        blank=True, null=True, upload_to="books", verbose_name="Зображення"
    )
    isbn = models.CharField(max_length=20, verbose_name="ISBN")
    author = models.ManyToManyField(Author, related_name="books", verbose_name="Автор")
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="books",
        verbose_name="Видавництво",
    )
    cateogry = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="books",
        verbose_name="Категорія",
    )
    cover = models.ForeignKey(
        Cover,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="book",
        verbose_name="Обкладинка",
    )
    language = models.ForeignKey(
        Language,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="books",
        verbose_name="Мова",
    )
    description = RichTextField(verbose_name="Опис")
    count = models.IntegerField(
        validators=[MinValueValidator(0)], verbose_name="Залишок", default=0
    )
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Ціна")
    discount = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True,
        blank=True,
        verbose_name="Знижка",
        default=0,
    )

    other_characteristics = models.ManyToManyField(
        OtherCharacteristic,
        null=True,
        blank=True,
        default=None,
        related_name="books",
        verbose_name="Інші Характеристики",
    )

    class Meta:
        ordering = ["title"]
        indexes = [
            models.Index(fields=["id", "slug"]),
            models.Index(fields=["title"]),
            models.Index(fields=["-created"]),
        ]

        verbose_name = "Книгу"
        verbose_name_plural = "Книги"

    @property
    def available(self):
        return True if self.count > 0 else False

    @property
    def is_discount(self):
        return True if self.discount > 0 else False

    @property
    def get_price_with_discount(self):
        return self.price * Decimal((1 - self.discount / 100))

    @property
    def get_authors(self):
        return ", ".join([author.name for author in self.author.all()])

    @property
    def short_description(self):
        return (
            self.description
            if len(self.description) < 297
            else f"{str(self.description)[:297]}..."
        )

    def get_absolute_url(self):
        return reverse("shop:book_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return f"{self.title}"
