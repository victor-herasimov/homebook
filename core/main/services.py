from django.db.models import QuerySet
from core.main.models import Address, Email, Info, Phone, Recommendations


class EmailService:
    model = Email

    def get_active_emails(self) -> QuerySet:
        return self.model.objects.filter(active=True)


class PhoneService:
    model = Phone

    def get_active_phones(self) -> QuerySet:
        return self.model.objects.filter(active=True)


class AddressService:
    model = Address

    def get_active_addresses(self) -> QuerySet:
        return self.model.objects.filter(active=True)


class RecommendationsService:
    model = Recommendations

    def get_active_recommendations(self) -> QuerySet:
        return self.model.objects.filter(show=True)


class InfoSerivice:
    model = Info

    def get_all(self) -> QuerySet:
        return self.model.objects.order_by("-created")
