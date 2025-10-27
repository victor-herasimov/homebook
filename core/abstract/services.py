from typing import Optional
from django.db.models import Model, QuerySet
from django.shortcuts import get_object_or_404


class AbstractService:
    model: Model = None

    def get_all(self) -> QuerySet:
        return self.model.objects.all()

    def get_by_slug(self, slug: str) -> Optional[Model]:
        return get_object_or_404(self.model, slug=slug)

    @classmethod
    def get_model(cls) -> Model:
        return cls.model
