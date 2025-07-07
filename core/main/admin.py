from django.contrib import admin
from .models import Recommendations


@admin.register(Recommendations)
class RecommendationsAdmin(admin.ModelAdmin):
    list_display = ["title", "book", "show"]
    fields = ["title", "image", "book", "show", "created", "updated"]
    readonly_fields = ["created", "updated"]
    list_editable = ["show"]
