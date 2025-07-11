from decimal import Decimal
import copy

from django.conf import settings
from django.http import HttpRequest
from django.contrib.sessions.backends.base import SessionBase

from core.shop.models import Book


class Cart:
    def __init__(self, request: HttpRequest) -> None:
        """
        Init Cart
        """
        self.session: SessionBase = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(
        self, book: Book, quantity: int = 1, override_quantity: bool = False
    ) -> None:
        """
        Add book to cart or update it quantity
        """
        book_id = str(book.id)
        if book_id not in self.cart:
            self.cart[book_id] = {
                "quantity": 0,
                "price": str(book.get_price_with_discount),
            }
        if override_quantity:
            self.cart[book_id]["quantity"] = quantity
        else:
            self.cart[book_id]["quantity"] += quantity
        self.save()

    def save(self) -> None:
        """
        Mark session as modifyed and save
        """
        self.session.modified = True

    def remove(self, book: Book) -> None:
        """
        Remove book from cart
        """
        book_id = str(book.id)
        if book_id in self.cart:
            del self.cart[book_id]
            self.save()

    def __iter__(self):
        """
        Iterration books position in cart
        """
        book_ids = self.cart.keys()
        books = Book.objects.filter(id__in=book_ids)
        cart = copy.deepcopy(self.cart)
        for book in books:
            cart[str(book.id)]["book"] = book
        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self) -> int:
        """
        Return length cart
        """
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self) -> Decimal:
        return sum(
            Decimal(item["price"]) * item["quantity"] for item in self.cart.values()
        )

    def clear(self) -> None:
        """
        Clear cart
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()
