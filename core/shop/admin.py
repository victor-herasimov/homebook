from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Category


@admin.register(Category)
class CateogryAdmin(MPTTModelAdmin):
    list_display = ["name", "updated", "created"]
    list_display_links = ["name"]
    fields = ["name", "slug", "parent", "updated", "created"]
    readonly_fields = ["updated", "created"]
    prepopulated_fields = {"slug": ["name"]}
    mptt_level_indent = 20
