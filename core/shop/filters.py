import math
from operator import ge
from django import forms
from django.db.utils import ProgrammingError
import django_filters
from django_property_filter import PropertyFilterSet, PropertyNumberFilter


from slugify import slugify

from .models import (
    Book,
    Cover,
    Language,
    OtherCharacteristic,
    OtherCharacteristicItem,
    Publisher,
    Author,
)


class ModelMultipleChoiceFieldCustomLabel(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.value}"


class ModelMultipleChoiceFilterCustomLabel(django_filters.ModelMultipleChoiceFilter):
    field_class = ModelMultipleChoiceFieldCustomLabel


def get_price_book():
    try:
        data = [book.get_price_with_discount for book in Book.objects.all()]
        return data if len(data) > 0 else [0]
    except Exception as e:
        print(type(e))
        return [0]


class BookFilter(PropertyFilterSet):
    author = django_filters.ModelMultipleChoiceFilter(
        queryset=Author.objects.order_by("name"),
        widget=forms.CheckboxSelectMultiple,
        field_name="author",
    )
    publisher = django_filters.ModelMultipleChoiceFilter(
        queryset=Publisher.objects.order_by("name"),
        widget=forms.CheckboxSelectMultiple,
        field_name="publisher",
    )
    cover = django_filters.ModelMultipleChoiceFilter(
        queryset=Cover.objects.order_by("cover"),
        widget=forms.CheckboxSelectMultiple,
        field_name="cover",
    )
    language = django_filters.ModelMultipleChoiceFilter(
        queryset=Language.objects.order_by("language"),
        widget=forms.CheckboxSelectMultiple,
        field_name="language",
    )

    price__gt = PropertyNumberFilter(
        field_name="get_price_with_discount",
        lookup_expr="gte",
        widget=forms.NumberInput(
            attrs={
                "type": "range",
                "id": "minPrice",
                "step": 1,
                "min": math.floor(
                    # min(book.get_price_with_discount for book in Book.objects.all())
                    min(get_price_book())
                ),
                "max": math.ceil(
                    # max(book.get_price_with_discount for book in Book.objects.all())
                    max(get_price_book())
                ),
                "initial": math.floor(
                    # min(book.get_price_with_discount for book in Book.objects.all())
                    min(get_price_book())
                ),
            },
        ),
        label="price",
    )
    price__lt = PropertyNumberFilter(
        field_name="get_price_with_discount",
        lookup_expr="lte",
        widget=forms.NumberInput(
            attrs={
                "type": "range",
                "id": "maxPrice",
                "step": 1,
                "min": math.floor(
                    # min(book.get_price_with_discount for book in Book.objects.all())
                    min(get_price_book())
                ),
                "max": math.ceil(
                    # max(book.get_price_with_discount for book in Book.objects.all())
                    max(get_price_book())
                ),
                "initial": math.ceil(
                    # max(book.get_price_with_discount for book in Book.objects.all())
                    max(get_price_book())
                ),
            },
        ),
        label="price",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        dynamic_fields = OtherCharacteristicItem.objects.all().distinct()
        for field_name in dynamic_fields:
            other_characteristic_ids = (
                OtherCharacteristic.objects.filter(item__name=field_name.name)
                .values_list("id", flat=True)
                .distinct(),
            )
            self.filters[slugify(str(field_name), separator="_")] = (
                ModelMultipleChoiceFilterCustomLabel(
                    queryset=OtherCharacteristic.objects.filter(
                        id__in=other_characteristic_ids
                    ),
                    widget=forms.CheckboxSelectMultiple,
                    field_name="other_characteristics",
                    label=field_name.name,
                )
            )

    class Meta:
        model = Book
        fields = [
            "price__gt",
            "price__lt",
            "author",
            "publisher",
            "cover",
            "language",
        ]
        exclude = ["price"]
