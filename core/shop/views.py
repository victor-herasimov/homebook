from decimal import Decimal
from django.core.exceptions import ImproperlyConfigured
from django.db.models import QuerySet, F, Case, When, BooleanField
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView
from django.utils.functional import cached_property
from django.conf import settings
from view_breadcrumbs import BaseBreadcrumbMixin

from django_filters.views import FilterView

from core.comment.forms import CommentForm
from core.shop.models import Book, Category
from .filters import BookFilter


class CatalogView(BaseBreadcrumbMixin, FilterView):
    model = Book
    template_name = "shop/catalog.html"
    context_object_name = "books"
    paginate_by = settings.ITEMS_PER_PAGE
    allow_empty = True
    # filterset_fields = ["author"]
    filterset_class = BookFilter

    @cached_property
    def crumbs(self):
        links = []

        category = get_object_or_404(Category, slug=self.kwargs["category_slug"])
        parent_categories = category.get_ancestors(include_self=True)
        links = [
            (category.name, reverse("shop:catalog", args=[category.slug]))
            for category in parent_categories
        ]

        return links

    def get_queryset(self):
        queryset = super().get_queryset()
        category = get_object_or_404(Category, slug=self.kwargs["category_slug"])
        category_ids = category.get_descendants(include_self=True).values_list(
            "id", flat=True
        )
        if category_ids:
            queryset = queryset.filter(cateogry__id__in=category_ids).all()
            queryset = queryset.annotate(
                is_available=Case(
                    When(count__gt=0, then=True),
                    When(count__exact=0, then=False),
                    default=True,
                    output_field=BooleanField(),
                )
            )
        return queryset.order_by("-is_available", "-updated")


class CatalogAllView(CatalogView):
    ordering = "-is_available", "-updated"

    @cached_property
    def crumbs(self):
        return [("Новинки", reverse("main:index"))]

    def get_queryset(self):
        if self.queryset is not None:
            queryset = self.queryset
            if isinstance(queryset, QuerySet):
                queryset = queryset.all()
        elif self.model is not None:
            queryset = self.model._default_manager.all()
        else:
            raise ImproperlyConfigured(
                "%(cls)s is missing a QuerySet. Define "
                "%(cls)s.model, %(cls)s.queryset, or override "
                "%(cls)s.get_queryset()." % {"cls": self.__class__.__name__}
            )
        queryset = queryset.annotate(
            is_available=Case(
                When(count__gt=0, then=True),
                When(count__exact=0, then=False),
                default=True,
                output_field=BooleanField(),
            )
        )
        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
        queryset = queryset.order_by(*ordering)
        return queryset


class CatalogBestPriceView(CatalogAllView):

    @cached_property
    def crumbs(self):
        return [("Кращі ціни", reverse("main:index"))]

    def get_queryset(self):
        queryset = super().get_queryset()
        # self.price * Decimal((1 - self.discount / 100))
        queryset = queryset.annotate(
            price_with_discount=F("price") - F("price") * F("discount") / 100,
            is_available=Case(
                When(count__gt=0, then=True),
                When(count__exact=0, then=False),
                default=True,
                output_field=BooleanField(),
            ),
        ).order_by("-is_available", "price_with_discount")
        return queryset


class BookView(BaseBreadcrumbMixin, DetailView):
    model = Book
    template_name = "shop/book-detail.html"
    context_object_name = "book"

    @cached_property
    def crumbs(self):
        book = self.get_object()
        category = book.cateogry
        parent_categories = category.get_ancestors(include_self=True)
        links = [
            (category.name, reverse("shop:catalog", args=[category.slug]))
            for category in parent_categories
        ] + [(book.title, book.get_absolute_url())]
        return links

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = CommentForm(
            initial={
                "user": (
                    self.request.user if not self.request.user.is_anonymous else ""
                ),
                "name": (
                    f"{self.request.user.first_name} {self.request.user.last_name}"
                    if not self.request.user.is_anonymous
                    else ""
                ),
                "book": self.get_object(),
                "rating": 1,
            }
        )
        return context


class SearchView(BaseBreadcrumbMixin, ListView):
    model = Book
    template_name = "shop/search.html"
    context_object_name = "books"

    def get_queryset(self):
        query = self.request.GET.get("q")

        # TODO make smart search

        if query:
            return self.model.objects.filter(title__icontains=query)
        return super().get_queryset()

    @cached_property
    def crumbs(self):
        return [("Пошук", reverse("shop:search"))]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q")
        return context


class SearchAjaxView(View):
    model = Book

    def get_queryset(self):
        query = self.request.GET.get("q")
        # TODO make smart search

        if query:
            return self.model.objects.filter(title__icontains=query)[:5]
        return []

    def get(self, request, *args, **kwargs):
        books = self.get_queryset()
        rendered_html = render_to_string(
            "components/_search_ajax_body.html",
            context={"books": books, "query": request.GET.get("q")},
            request=request,
        )
        print(rendered_html)
        return JsonResponse({"body": rendered_html.strip()})
