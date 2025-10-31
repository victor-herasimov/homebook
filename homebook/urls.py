from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path("", include("core.main.urls", namespace="main")),
    path("catalog/", include("core.shop.urls", namespace="shop")),
    path("cart/", include("core.cart.urls", namespace="cart")),
    path("orders/", include("core.orders.urls", namespace="orders")),
    path("account/", include("core.account.urls", namespace="account")),
    path("comment/", include("core.comment.urls", namespace="comments")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += debug_toolbar_urls()
