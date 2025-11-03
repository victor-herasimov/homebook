from django.urls import reverse
from django.views.generic import DetailView, TemplateView
from view_breadcrumbs import BaseBreadcrumbMixin

from core.main.models import Document
from core.main.services import (
    AddressService,
    EmailService,
    InfoSerivice,
    PhoneService,
    RecommendationsService,
)

from core.shop.services import BookService


class ContactView(BaseBreadcrumbMixin, TemplateView):
    template_name = "main/contact.html"
    extra_context = {"title": "Контакти"}

    @property
    def crumbs(self):
        return [("Контакти", reverse("main:index"))]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["emails"] = EmailService().get_active_emails()
        context["phones"] = PhoneService().get_active_phones()
        context["addresses"] = AddressService().get_active_addresses()
        return context


class IndexView(TemplateView):
    template_name = "main/index.html"
    extra_context = {"title": "Головна"}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recommendations"] = (
            RecommendationsService().get_active_recommendations()
        )
        context["new_books"] = BookService().get_new_books()
        context["informations"] = InfoSerivice().get_all()
        return context


class DocumentView(BaseBreadcrumbMixin, DetailView):
    model = Document
    template_name = "main/information.html"
    context_object_name = "document"

    @property
    def crumbs(self):
        document = self.get_object()
        return [
            (document.title, reverse("main:information", kwargs={"pk": document.id}))
        ]
