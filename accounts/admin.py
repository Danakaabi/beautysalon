from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, OTP


# ==========================================================
# 🧑‍💼 Admin Panel — Custom User
# ==========================================================
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # الأعمدة اللي تظهر في صفحة جميع المستخدمين
    list_display = ("phone", "name", "is_staff", "is_superuser", "is_active", "date_joined")
    list_filter = ("is_staff", "is_superuser", "is_active")

    # كيفية عرض البيانات داخل صفحة تفاصيل المستخدم
    fieldsets = (
        ("بيانات الدخول", {"fields": ("phone", "password")}),
        ("المعلومات الشخصية", {"fields": ("name",)}),
        ("الصلاحيات", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("تواريخ مهمة", {"fields": ("last_login", "date_joined")}),
    )

    # عند إضافة مستخدم جديد عبر لوحة الأدمن
    add_fieldsets = (
        ("إنشاء مستخدم جديد", {
            "classes": ("wide",),
            "fields": ("phone", "password1", "password2", "is_staff", "is_superuser", "is_active"),
        }),
    )

    search_fields = ("phone", "name")
    ordering = ("phone",)


# ==========================================================
# 🔢 Admin Panel — OTP Codes
# ==========================================================
@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ("phone", "code", "created_at")
    search_fields = ("phone", "code")
    readonly_fields = ("created_at",)
