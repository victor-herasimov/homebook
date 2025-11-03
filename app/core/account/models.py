from django.core.validators import EmailValidator
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)

from core.orders.validators import PhoneNumberValidator


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        """
        Create and return a User with an email, password, phone number
        """
        if email is None:
            raise TypeError("Users must have a email")
        if password is None:
            raise TypeError("Users must have a password")
        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **kwargs):
        """
        Create and return User with superuser (admin) permissions
        """
        user = self.create_user(email, phone=None, password=password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(
        max_length=20,
        verbose_name="Телефон",
        unique=False,
        blank=True,
        null=True,
        validators=[PhoneNumberValidator()],
    )
    first_name = models.CharField(max_length=255, verbose_name="Ім'я")
    last_name = models.CharField(max_length=255, verbose_name="Прізвище")
    email = models.EmailField(
        max_length=256, unique=True, validators=[EmailValidator()], verbose_name="Email"
    )
    delivery_address = models.CharField(
        max_length=512, blank=True, null=True, verbose_name="Адреса доставки"
    )

    is_active = models.BooleanField(default=True, verbose_name="Активний")
    is_staff = models.BooleanField(default=False, verbose_name="Співробітник")
    created = models.DateTimeField(auto_now=True, verbose_name="Дата створення")
    updated = models.DateTimeField(auto_now_add=True, verbose_name="Дата оновлення")

    USERNAME_FIELD = "email"

    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Користувач"
        verbose_name_plural = "Користувачі"
        ordering = ["email"]
