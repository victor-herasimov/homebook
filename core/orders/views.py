from django.shortcuts import render
from django.views.generic import FormView

from core.cart.cart import Cart
from .models import OrderItem
from .forms import OrderCreateForm


class OrderView(FormView):
    template_name = "orders/order/create.html"
    form_class = OrderCreateForm
