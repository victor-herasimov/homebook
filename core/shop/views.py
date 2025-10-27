from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView
from django.conf import settings
from view_breadcrumbs import BaseBreadcrumbMixin

from django_filters.views import FilterView

from core.comment.forms import CommentForm
from core.shop.services import CategoryService, BookService
from .filters import BookFilter


class CatalogView(BaseBreadcrumbMixin, FilterView):
    template_name = "shop/catalog.html"
    context_object_name = "books"
    paginate_by = settings.ITEMS_PER_PAGE
    allow_empty = True
    filterset_class = BookFilter

    @property
    def crumbs(self):
        parent_categories = CategoryService().get_parent_categories_by_slug(
            self.kwargs["category_slug"]
        )
        return [
            (category.name, reverse("shop:catalog", args=[category.slug]))
            for category in parent_categories
        ]

    def get_queryset(self):
        category_ids = CategoryService().get_category_descendants_ids_by_category_slug(
            self.kwargs["category_slug"]
        )
        if category_ids:
            queryset = BookService().get_queryset_by_category_ids(category_ids)
            return BookService().order_by_descent_available_and_updated(queryset)
        return BookService().get_all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = (
            CategoryService().get_by_slug(self.kwargs["category_slug"]).name
        )
        return context


class CatalogAllView(BaseBreadcrumbMixin, FilterView):
    template_name = "shop/catalog.html"
    context_object_name = "books"
    paginate_by = settings.ITEMS_PER_PAGE
    allow_empty = True
    filterset_class = BookFilter

    @property
    def crumbs(self):
        return [("Новинки", reverse("main:index"))]

    def get_queryset(self):
        print("queryset all")
        return BookService().order_by_descent_available_and_updated(
            BookService().get_all()
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Новинки"
        return context


class CatalogBestPriceView(BaseBreadcrumbMixin, FilterView):
    template_name = "shop/catalog.html"
    context_object_name = "books"
    paginate_by = settings.ITEMS_PER_PAGE
    allow_empty = True
    filterset_class = BookFilter

    @property
    def crumbs(self):
        return [("Кращі ціни", reverse("main:index"))]

    def get_queryset(self):
        return BookService().order_by_descent_available_and_ascending_price(
            BookService().get_all()
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Кращі ціни"
        return context


class BookView(BaseBreadcrumbMixin, DetailView):
    model = BookService().get_model()
    template_name = "shop/book-detail.html"
    context_object_name = "book"

    @property
    def crumbs(self):
        book = self.get_object()
        parent_categories = CategoryService().get_parent_categories(book.cateogry)
        return [
            (category.name, reverse("shop:catalog", args=[category.slug]))
            for category in parent_categories
        ] + [(book.title, book.get_absolute_url())]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
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
                "book": book,
                "rating": 1,
            }
        )
        context["title"] = book.title
        return context


class SearchView(BaseBreadcrumbMixin, ListView):
    template_name = "shop/search.html"
    context_object_name = "books"
    paginate_by = settings.ITEMS_PER_PAGE

    @property
    def crumbs(self):
        return [("Пошук", reverse("shop:search"))]

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            return BookService().search_by_query(query)
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q")
        return context


class SearchAjaxView(View):
    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            return BookService().search_by_query(query)[:5]
        return []

    def get(self, request, *args, **kwargs):
        books = self.get_queryset()
        rendered_html = render_to_string(
            "components/_search_ajax_body.html",
            context={"books": books, "query": request.GET.get("q")},
            request=request,
        )
        return JsonResponse({"body": rendered_html.strip()})
