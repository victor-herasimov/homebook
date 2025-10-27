from .services import CategoryService


def main_catalog(request):
    return {"main_catalog": CategoryService().get_all()}
