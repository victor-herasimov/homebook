from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView, TemplateView
from view_breadcrumbs import BaseBreadcrumbMixin
from core.orders.services import OrderService

from .forms import OrderCreateForm


class OrderView(BaseBreadcrumbMixin, FormView):
    template_name = "orders/order/create.html"
    form_class = OrderCreateForm

    @property
    def crumbs(self):
        return [("Оформлення замовлення", reverse("main:index"))]

    def get_initial(self):
        user = self.request.user
        if not user.is_anonymous:
            return {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "phone": user.phone,
                "email": user.email,
                "delivery_address": user.delivery_address,
            }
        return super().get_initial()

    def form_valid(self, form):
        order = OrderService().create_order(self.request, form)
        return redirect(reverse("orders:order_success", args=[order.id]))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Оформлення замовлення"
        return context


class OrderSuccess(BaseBreadcrumbMixin, TemplateView):
    template_name = "orders/order/success.html"

    @property
    def crumbs(self):
        return [("Замовлення успішне", reverse("main:index"))]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["order_id"] = self.kwargs["order_id"]
        context["title"] = "Замовлення успішне"
        return context
