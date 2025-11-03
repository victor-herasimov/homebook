from django.http import HttpRequest
from .cart import Cart


def cart(request: HttpRequest) -> Cart:
    return {"cart": Cart(request)}
