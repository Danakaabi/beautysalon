from pathlib import Path
import os

# ==========================================================
# 📂 BASE DIRECTORY
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ==========================================================
# 🚨 SECURITY
# ==========================================================

# ❗️ غيّري هذا المفتاح فوراً — لا تستخدمي المفتاح القديم أبداً
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "CHANGE_ME")

DEBUG = True

ALLOWED_HOSTS = ["*"]   # أثناء التطوير فقط


# ==========================================================
# 🧩 INSTALLED APPS
# ==========================================================

INSTALLED_APPS = [
    # Django default apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # 💄 Salon custom apps
    "accounts",
    "catalog",
    "scheduling",
    "bookings",
    "billing",
    "notifications_center",
    "portal_client",
    "control_panel",
]


# ==========================================================
# 🔧 MIDDLEWARE
# ==========================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",

    # لدعم RTL واللغات
    "django.middleware.locale.LocaleMiddleware",

    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ==========================================================
# 🌐 URLS + WSGI
# ==========================================================

ROOT_URLCONF = "salon_project.urls"
WSGI_APPLICATION = "salon_project.wsgi.application"


# ==========================================================
# 🎨 TEMPLATES CONFIG
# ==========================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",

        # ⭐ إضافة مسار صفحة الداشبورد هنا ⭐
        "DIRS": [
            BASE_DIR / "templates",
            "/Users/hlm../salon_project/templates/",
        ],

        "APP_DIRS": True,

        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# ==========================================================
# 🗄 DATABASE
# ==========================================================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# ==========================================================
# 🔐 PASSWORD VALIDATORS
# ==========================================================

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# ==========================================================
# 🌍 INTERNATIONALIZATION
# ==========================================================

LANGUAGE_CODE = "ar"
TIME_ZONE = "Asia/Riyadh"

USE_I18N = True
USE_TZ = True


# ==========================================================
# 🎨 STATIC FILES
# ==========================================================

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"


# ==========================================================
# 🖼 MEDIA FILES
# ==========================================================

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# ==========================================================
# 👤 CUSTOM USER MODEL
# ==========================================================

AUTH_USER_MODEL = "accounts.CustomUser"


# ==========================================================
# 🔑 DEFAULT FIELD TYPE
# ==========================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
