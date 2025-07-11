from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path("add/<int:book_id>", views.CartAdd.as_view(), name="add"),
]
