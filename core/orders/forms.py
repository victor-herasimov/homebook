from django import forms

from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "user",
            "first_name",
            "last_name",
            "phone",
            "email",
            "delivery_address",
            "comment",
        ]
