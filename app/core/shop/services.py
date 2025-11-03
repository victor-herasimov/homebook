from django.db.models import F, BooleanField, Case, Prefetch, QuerySet, When
from django.contrib.postgres.search import SearchVector, SearchRank, SearchQuery
from django.http import Http404
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

    def get_category_descendants_ids_by_category(self, category: Category) -> list[int]:
        return category.get_descendants(include_self=True).values_list("id", flat=True)


class BookService(AbstractService):
    model = Book

    def get_by_slug(self, slug: str) -> QuerySet:
        queryset = (
            self.model.objects.select_related(
                "publisher",
                "cateogry",
                "cover",
                "language",
            )
            .prefetch_related(
                Prefetch(
                    "other_characteristics",
                    queryset=OtherCharacteristic.objects.select_related("item"),
                )
            )
            .prefetch_related("author")
            .filter(slug=slug)
        )
        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404()
        return obj

    def get_new_books(self, count: int = 5) -> QuerySet:
        return self.model.objects.filter(count__gt=0).order_by("-updated")[:count]

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


class AuthorService:
    model = Author

    def get_queryset_order_by_name(self) -> QuerySet:
        return self.model.objects.order_by("name")


class PublisherService:
    model = Publisher

    def get_queryset_order_by_name(self) -> QuerySet:
        return self.model.objects.order_by("name")


class CoverService:
    model = Cover

    def get_queryset_order_by_cover(self) -> QuerySet:
        return self.model.objects.order_by("cover")


class LanguageService:
    model = Language

    def get_queryset_order_by_language(self) -> QuerySet:
        return self.model.objects.order_by("language")


class OtherCharacteristicItemService:
    model = OtherCharacteristicItem

    def get_all(self) -> QuerySet:
        return self.model.objects.prefetch_related(Prefetch("items")).all()


class OtherCharacteristicService:
    model = OtherCharacteristic

    def get_other_characteristic_ids_by_item_name(self, name) -> list[int]:
        return (
            self.model.objects.select_related("item")
            .filter(item__name=name)
            .values_list("id", flat=True)
            .distinct()
        )

    def get_queryset_by_ids(self, ids: list[int]) -> QuerySet:
        return self.model.objects.select_related("item").filter(id__in=ids)
