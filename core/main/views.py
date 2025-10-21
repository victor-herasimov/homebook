from django.urls import reverse
from django.utils.functional import cached_property
from django.views.generic import DetailView, TemplateView
from view_breadcrumbs import BaseBreadcrumbMixin

from core.main.models import Info, Recommendations, Document, Address, Phone, Email
from core.shop.models import Book


class ContactView(TemplateView):
    template_name = "main/contact.html"
    extra_context = {"title": "Контакти"}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["emails"] = Email.objects.filter(active=True).all()
        context["phones"] = Phone.objects.filter(active=True).all()
        context["addresses"] = Address.objects.filter(active=True).all()
        return context


class IndexView(TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recommendations"] = Recommendations.objects.filter(show=True).all()
        context["new_books"] = (
            Book.objects.filter(count__gt=0).order_by("-updated").all()[:5]
        )
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
