from django.contrib import admin
from .models import Recommendations, Info, Document, Phone, Address, Email


admin.site.site_header = "HomeBook"
admin.site.site_title = "HomeBook"
admin.site.index_title = "Адміністрування HomeBook"


@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    list_display = ["phone", "active"]
    fields = ["id", "phone", "active"]
    list_editable = ["active"]
    readonly_fields = ["id"]
    list_display_links = ["phone"]


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ["email", "active"]
    fields = ["id", "email", "active"]
    list_editable = ["active"]
    readonly_fields = ["id"]
    list_display_links = ["email"]


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ["address", "active"]
    fields = ["id", "address", "active"]
    list_editable = ["active"]
    readonly_fields = ["id"]
    list_display_links = ["address"]


@admin.register(Recommendations)
class RecommendationsAdmin(admin.ModelAdmin):
    list_display = ["title", "book", "show"]
    fields = ["title", "image", "book", "show", "created", "updated"]
    readonly_fields = ["created", "updated"]
    list_editable = ["show"]


@admin.register(Info)
class InfoAdmin(admin.ModelAdmin):
    list_display = ["id", "created", "updated"]
    fields = ["text", "created", "updated"]
    readonly_fields = ["created", "updated"]


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "created", "updated"]
    fields = ["id", "title", "text", "created", "updated"]
    readonly_fields = ["id", "created", "updated"]
