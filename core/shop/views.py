from django.views.generic import ListView

from core.shop.models import Category


class CatalogView(ListView):
    model = Category
    template_name = "shop/catalog.html"
