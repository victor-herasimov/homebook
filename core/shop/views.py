from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View
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
