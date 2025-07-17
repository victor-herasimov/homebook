from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [
    path("search/", views.SearchView.as_view(), name="search"),
    path("ajax-search/", views.SearchAjaxView.as_view(), name="ajax-search"),
    path("<slug:category_slug>/", views.CatalogView.as_view(), name="catalog"),
    path("books/<slug:slug>/", views.BookView.as_view(), name="book_detail"),
]
