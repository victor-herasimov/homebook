from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [
    path("<slug:category_slug>/", views.CatalogView.as_view(), name="catalog"),
]
