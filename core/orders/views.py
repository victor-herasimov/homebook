from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView, TemplateView
from django.db import transaction

from core.cart.cart import Cart
from .models import OrderItem
from .forms import OrderCreateForm


class OrderView(FormView):
    template_name = "orders/order/create.html"
    form_class = OrderCreateForm

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
        with transaction.atomic():
            cart = Cart(self.request)
            order = form.save()
            for item in cart:
                book = item["book"]
                OrderItem.objects.create(
                    order=order,
                    book=book,
                    price=item["price"],
                    quantity=item["quantity"],
                )
                # book.count -= item["quantity"]
            cart.clear()
            return redirect(reverse("orders:order_success", args=[order.id]))


class OrderSuccess(TemplateView):
    template_name = "orders/order/success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["order_id"] = self.kwargs["order_id"]
        return context
