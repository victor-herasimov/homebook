from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from core.shop.models import Book, Category


class CatalogView(ListView):
    model = Book
    template_name = "shop/catalog.html"
    context_object_name = "books"

    def get_queryset(self):
        category = get_object_or_404(Category, slug=self.kwargs["category_slug"])
        category_ids = category.get_descendants(include_self=True).values_list(
            "id", flat=True
        )
        queryset = Book.objects.filter(cateogry__id__in=category_ids).all()
        return queryset
