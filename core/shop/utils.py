from core.shop.services import BookService


def get_price_book():
    try:
        data = [book.get_price_with_discount for book in BookService().get_all()]
        return data if len(data) > 0 else [0]
    except Exception as e:
        print(type(e))
        return [0]
