from .models import Category


def main_catalog(request):
    return {"main_catalog": Category.objects.all()}
