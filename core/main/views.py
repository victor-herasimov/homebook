from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404

from core.main.models import Info, Recommendations
from core.shop.models import Book, Category


class IndexView(TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recommendations"] = Recommendations.objects.filter(show=True).all()
        context["new_books"] = Book.objects.order_by("-updated").all()[:5]
        category = get_object_or_404(Category, slug="komplekti-knig")
        category_ids = category.get_descendants(include_self=True).values_list(
            "id", flat=True
        )
        context["set_books"] = Book.objects.filter(cateogry__id__in=category_ids).all()[
            :5
        ]
        context["informations"] = Info.objects.order_by("created").all()
        return context
