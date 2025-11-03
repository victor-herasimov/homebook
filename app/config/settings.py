import os
from pathlib import Path
from re import DEBUG
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    "SECRET_KEY", "django-insecure-ouvla@=_z^oa9&f$tx^=^ga7+7e2kg9m5lqe#nn7+$%&6!60l6"
)

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
# SECURE_SSL_REDIRECT = True


DEBUG = bool(int(os.environ.get("DEBUG", 1)))


if DEBUG:
    ALLOWED_HOSTS = []
else:
    ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split(" ")


# Application definition

INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.humanize",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    # Installed apps
    "mptt",
    "view_breadcrumbs",
    "ckeditor",
    "django_filters",
    "django_property_filter",
    "debug_toolbar",
    # My applicatios
    "core",
    "core.main.apps.MainConfig",
    "core.shop.apps.ShopConfig",
    "core.cart.apps.CartConfig",
    "core.orders.apps.OrdersConfig",
    "core.account.apps.AccountConfig",
    "core.comment.apps.CommentConfig",
]


MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.shop.context_processors.main_catalog",
                "core.cart.context_processors.cart",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.environ.get("DATABASE_HOST"),
        "PORT": os.getenv("DATABASE_PORT"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


INTERNAL_IPS = [
    "127.0.0.1",
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "uk-uk"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / STATIC_URL]
# STATIC_ROOT = BASE_DIR / STATIC_URL

# Media files
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / MEDIA_URL

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Breadcrumbs
BREADCRUMBS_HOME_LABEL = "HomeBook"
BREADCRUMBS_TEMPLATE = "components/_breadcrumbs.html"

# ckeitor
CKEDITOR_UPLOAD_PATH = "media/"

# cart
CART_SESSION_ID = "cart"

# Paginations
ITEMS_PER_PAGE = 8
COMMENTS_PER_PAGE = 8

# Account
AUTH_USER_MODEL = "core_account.User"
LOGIN_URL = "/account/login/"

# Email
if bool(int(os.environ.get("DEVELOP_EMAIL_SERVER"))):
    EMAIL_HOST = os.environ.get("MAILDEV_WEB_HOST")
    EMAIL_PORT = os.environ.get("MAILDEV_WEB_PORT")
else:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = os.environ.get("EMAIL_HOST")
    EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
    EMAIL_PORT = os.environ.get("EMAIL_PORT")
    # EMAIL_USE_TLS = bool(os.environ.get("EMAIL_USE_TLS"))
    EMAIL_USE_SSL = bool(os.environ.get("EMAIL_USE_SSL"))
    DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL")

# Celery settings
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")

SILENCED_SYSTEM_CHECKS = [
    "ckeditor.W001",
]
