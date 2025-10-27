from django.db.models import F, BooleanField, Case, QuerySet, When
from django.contrib.postgres.search import SearchVector, SearchRank, SearchQuery
from mptt.querysets import TreeQuerySet
from mptt.models import MPTTModel
from core.abstract.services import AbstractService
from core.shop.models import (
    Author,
    Category,
    Book,
    Cover,
    Language,
    OtherCharacteristic,
    OtherCharacteristicItem,
    Publisher,
)


class CategoryService(AbstractService):
    model: MPTTModel = Category

    def get_parent_categories(self, category: Category) -> TreeQuerySet:
        return category.get_ancestors(include_self=True)

    def get_parent_categories_by_slug(self, slug: str) -> TreeQuerySet:
        return self.get_parent_categories(self.get_by_slug(slug))

    def get_category_descendants_ids_by_category_slug(self, slug: str) -> list[int]:
        return (
            self.get_by_slug(slug)
            .get_descendants(include_self=True)
            .values_list("id", flat=True)
        )


class BookService(AbstractService):
    model = Book

    def get_queryset_by_category_ids(self, category_ids: list[int]) -> QuerySet:
        return self.model.objects.filter(cateogry__id__in=category_ids).all()

    def order_by_descent_available_and_updated(self, queryset) -> QuerySet:
        return queryset.annotate(
            is_available=Case(
                When(count__gt=0, then=True),
                When(count__exact=0, then=False),
                default=True,
                output_field=BooleanField(),
            )
        ).order_by("-is_available", "-updated")

    def order_by_descent_available_and_ascending_price(self, queryset) -> QuerySet:
        return queryset.annotate(
            price_with_discount=F("price") - F("price") * F("discount") / 100,
            is_available=Case(
                When(count__gt=0, then=True),
                When(count__exact=0, then=False),
                default=True,
                output_field=BooleanField(),
            ),
        ).order_by(
            "-is_available",
            "price_with_discount",
        )

    def search_by_query(self, query: str) -> QuerySet:
        search_vector = SearchVector(
            "title", "description", "author__name", "publisher__name"
        )
        search_query = SearchQuery(query)
        return (
            self.model.objects.annotate(
                search=search_vector, rank=SearchRank(search_vector, search_query)
            )
            .filter(search=search_query)
            .order_by("-rank")
        )


class AuthorService(AbstractService):
    model = Author

    def get_queryset_order_by_name(self) -> QuerySet:
        return self.model.objects.order_by("name")


class PublisherService(AbstractService):
    model = Publisher

    def get_queryset_order_by_name(self) -> QuerySet:
        return self.model.objects.order_by("name")


class CoverService(AbstractService):
    model = Cover

    def get_queryset_order_by_cover(self) -> QuerySet:
        return self.model.objects.order_by("cover")


class LanguageService(AbstractService):
    model = Language

    def get_queryset_order_by_language(self) -> QuerySet:
        return self.model.objects.order_by("language")


class OtherCharacteristicItemService(AbstractService):
    model = OtherCharacteristicItem

    def get_all_distinct(self) -> QuerySet:
        return self.model.objects.all().distinct()


class OtherCharacteristicService(AbstractService):
    model = OtherCharacteristic

    def get_other_characteristic_ids_by_item_name(self, name) -> list[int]:
        return (
            self.model.objects.filter(item__name=name)
            .values_list("id", flat=True)
            .distinct()
        )

    def get_queryset_by_ids(self, ids: list[int]) -> QuerySet:
        return self.model.objects.filter(id__in=ids)
