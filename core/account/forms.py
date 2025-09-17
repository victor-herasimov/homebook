from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    UserChangeForm,
)

from core.account.models import User
from core.orders.validators import PhoneNumberValidator


class UserLoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ["email", "password"]


class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = (
            "email",
            "password1",
            "password2",
            "first_name",
            "last_name",
            "phone",
            "delivery_address",
        )

    email = forms.CharField()
    password1 = forms.CharField()
    password2 = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    phone = forms.CharField(validators=[PhoneNumberValidator])
    delivery_address = forms.CharField()

    def clean_password2(self):
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError("Паролі не співпадають")
        return password2


class UserChangeInfoForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "phone",
        )

    email = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    phone = forms.CharField(validators=[PhoneNumberValidator])
