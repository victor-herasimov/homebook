from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("create/", views.OrderView.as_view(), name="order_create"),
    path("success/<int:order_id>/", views.OrderSuccess.as_view(), name="order_success"),
]
