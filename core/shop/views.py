from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.utils.functional import cached_property
from view_breadcrumbs import BaseBreadcrumbMixin

from core.shop.models import Book, Category


class CatalogView(BaseBreadcrumbMixin, ListView):
    model = Book
    template_name = "shop/catalog.html"
    context_object_name = "books"

    @cached_property
    def crumbs(self):
        category = get_object_or_404(Category, slug=self.kwargs["category_slug"])
        parent_categories = category.get_ancestors(include_self=True)
        links = [
            (category.name, reverse("shop:catalog", args=[category.slug]))
            for category in parent_categories
        ]
        return links

    def get_queryset(self):
        category = get_object_or_404(Category, slug=self.kwargs["category_slug"])
        category_ids = category.get_descendants(include_self=True).values_list(
            "id", flat=True
        )
        queryset = Book.objects.filter(cateogry__id__in=category_ids).all()
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
