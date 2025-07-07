from django.contrib import admin
from django.utils.safestring import mark_safe
from mptt.admin import MPTTModelAdmin
from .models import (
    Category,
    Publisher,
    Author,
    Language,
    Cover,
    OtherCharacteristicItem,
    OtherCharacteristic,
    Book,
)


@admin.register(Category)
class CateogryAdmin(MPTTModelAdmin):
    list_display = ["name", "updated", "created"]
    list_display_links = ["name"]
    fields = ["name", "slug", "parent", "updated", "created"]
    readonly_fields = ["updated", "created"]
    prepopulated_fields = {"slug": ["name"]}
    mptt_level_indent = 20


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["name", "updated", "created"]
    list_display_links = ["name"]
    fields = ["name", "slug", "updated", "created"]
    readonly_fields = ["updated", "created"]
    prepopulated_fields = {"slug": ["name"]}


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ["name", "updated", "created"]
    list_display_links = ["name"]
    fields = ["name", "slug", "updated", "created"]
    readonly_fields = ["updated", "created"]
    prepopulated_fields = {"slug": ["name"]}


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ["language", "updated", "created"]
    list_display_links = ["language"]
    fields = ["language", "slug", "updated", "created"]
    readonly_fields = ["updated", "created"]
    prepopulated_fields = {"slug": ["language"]}


@admin.register(Cover)
class CoverAdmin(admin.ModelAdmin):
    list_display = ["cover", "updated", "created"]
    list_display_links = ["cover"]
    fields = ["cover", "slug", "updated", "created"]
    readonly_fields = ["updated", "created"]
    prepopulated_fields = {"slug": ["cover"]}


@admin.register(OtherCharacteristicItem)
class OtherCharacteristicItemAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_display_links = ["name"]
    fields = ["name"]


@admin.register(OtherCharacteristic)
class OtherCharacteristicAdmin(admin.ModelAdmin):
    list_display = ["item", "value"]
    list_display_links = ["item", "value"]
    fields = ["item", "value", "books"]


class OtherCharacteristicInline(admin.TabularInline):
    model = OtherCharacteristic
    extra = 1


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):

    def thumbnail(self, obj):

        return (
            mark_safe(f'<img src="{obj.image.url}" width="60" height="60"')
            if obj.image
            else "-"
        )

    thumbnail.short_description = "Image"

    def get_authors(self, obj):
        return ", ".join([a.name for a in obj.author.all()])

    get_authors.short_description = "Автори"

    list_display = ["title", "thumbnail", "get_authors", "isbn", "cateogry"]
    list_display_links = ["title", "thumbnail"]
    list_filter = ["author", "cateogry", "language"]
    inlines = [OtherCharacteristicInline]
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "title",
                    "image",
                    "thumbnail",
                    "isbn",
                    "author",
                    "publisher",
                    "cateogry",
                    "language",
                    "cover",
                ]
            },
        ),
        (
            "Ціна - Залишки",
            {
                "fields": [
                    (
                        "price",
                        "discount",
                    ),
                    "count",
                ]
            },
        ),
        (
            "Опис",
            {"fields": ["description"]},
        ),
    ]
    readonly_fields = ["thumbnail"]
