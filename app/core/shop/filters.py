import math
from django import forms
import django_filters
from django_property_filter import PropertyFilterSet, PropertyNumberFilter

from slugify import slugify

from core.shop.models import OtherCharacteristic, OtherCharacteristicItem
from core.shop.services import (
    AuthorService,
    BookService,
    CoverService,
    LanguageService,
    OtherCharacteristicItemService,
    OtherCharacteristicService,
    PublisherService,
)
from core.shop.utils import get_price_book


class ModelMultipleChoiceFieldCustomLabel(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.value}"


class ModelMultipleChoiceFilterCustomLabel(django_filters.ModelMultipleChoiceFilter):
    field_class = ModelMultipleChoiceFieldCustomLabel


class BookFilter(PropertyFilterSet):
    author = django_filters.ModelMultipleChoiceFilter(
        queryset=AuthorService().get_queryset_order_by_name(),
        widget=forms.CheckboxSelectMultiple,
        field_name="author",
    )
    publisher = django_filters.ModelMultipleChoiceFilter(
        queryset=PublisherService().get_queryset_order_by_name(),
        widget=forms.CheckboxSelectMultiple,
        field_name="publisher",
    )
    cover = django_filters.ModelMultipleChoiceFilter(
        queryset=CoverService().get_queryset_order_by_cover(),
        widget=forms.CheckboxSelectMultiple,
        field_name="cover",
    )
    language = django_filters.ModelMultipleChoiceFilter(
        queryset=LanguageService().get_queryset_order_by_language(),
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
                "min": math.floor(min(get_price_book())),
                "max": math.ceil(max(get_price_book())),
                "initial": math.floor(min(get_price_book())),
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
                "min": math.floor(min(get_price_book())),
                "max": math.ceil(max(get_price_book())),
                "initial": math.ceil(max(get_price_book())),
            },
        ),
        label="price",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        dynamic_fields = OtherCharacteristicItemService().get_all()
        for field_name in dynamic_fields:
            self.filters[slugify(str(field_name), separator="_")] = (
                ModelMultipleChoiceFilterCustomLabel(
                    queryset=field_name.items.order_by("value").all(),
                    widget=forms.CheckboxSelectMultiple,
                    field_name="other_characteristics",
                    label=field_name.name,
                )
            )

    class Meta:
        model = BookService().get_model()
        fields = [
            "price__gt",
            "price__lt",
            "author",
            "publisher",
            "cover",
            "language",
        ]
        exclude = ["price"]
