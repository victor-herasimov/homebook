from django.urls import reverse
from django.utils.functional import cached_property
from django.views.generic import DetailView, TemplateView
from django.shortcuts import get_object_or_404
from view_breadcrumbs import BaseBreadcrumbMixin

from core.main.models import Info, Recommendations, Document
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


class DocumentView(BaseBreadcrumbMixin, DetailView):
    model = Document
    template_name = "main/information.html"
    context_object_name = "document"

    @cached_property
    def crumbs(self):
        object = self.get_object()
        return [(object.title, reverse("main:information", kwargs={"pk": object.id}))]
