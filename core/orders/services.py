from django.db import transaction
from django.http import HttpRequest
from core.cart.cart import Cart
from core.orders.forms import OrderCreateForm
from core.orders.models import Order, OrderItem


class OrderItemService:
    model = OrderItem

    def create(self, **kwargs) -> OrderItem:
        return OrderItem.objects.create(**kwargs)


class OrderService:
    model = Order

    def create_order(self, request: HttpRequest, form: OrderCreateForm) -> Order:
        with transaction.atomic():
            cart = Cart(request)
            order = form.save(commit=False)
            if not request.user.is_anonymous:
                order.user = request.user
            order.save()
            for item in cart:
                book = item["book"]
                OrderItemService().create(
                    order=order,
                    book=book,
                    price=item["price"],
                    quantity=item["quantity"],
                )
                # book.count -= item["quantity"]
            cart.clear()
        return order
