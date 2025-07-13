from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.views.generic import View

from core.cart.forms import CartAddForm
from core.shop.models import Book

from .cart import Cart


class CartAdd(View):
    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        book = get_object_or_404(Book, id=self.kwargs.get("book_id"))
        form = CartAddForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(
                book=book, quantity=cd["quantity"], override_quantity=cd["override"]
            )
        return JsonResponse(
            {
                "cart_body": render_to_string(
                    "components/_cart_body.html", {"cart": cart}, request=request
                ),
                "cart_quantity": len(cart),
                "total_price": float(cart.get_total_price()),
                "is_empty": not bool(cart),
            },
        )


class CartRemove(View):
    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        book = get_object_or_404(Book, id=self.kwargs.get("book_id"))
        cart.remove(book)
        return JsonResponse(
            {
                "cart_body": render_to_string(
                    "components/_cart_body.html", {"cart": cart}, request=request
                ),
                "cart_quantity": len(cart),
                "total_price": float(cart.get_total_price()),
                "is_empty": not bool(cart),
            },
        )
