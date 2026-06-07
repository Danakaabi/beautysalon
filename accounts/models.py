from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


# ==========================================================
# 🔐 Custom User Manager
# ==========================================================
class CustomUserManager(BaseUserManager):

    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError("يجب إدخال رقم الجوال")

        phone = str(phone).strip()

        user = self.model(phone=phone, **extra_fields)

        # كلمة المرور (تُستخدم فقط للأدمن)
        user.set_password(password or self.make_random_password())

        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not password:
            raise ValueError("يجب تعيين كلمة مرور للمشرف")

        return self.create_user(phone, password, **extra_fields)


# ==========================================================
# 👤 Custom User Model (Login by Phone)
# ==========================================================
class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="رقم الجوال"
    )

    name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="الاسم"
    )

    # صلاحيات
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.phone

    class Meta:
        verbose_name = "مستخدم"
        verbose_name_plural = "المستخدمون"


# ==========================================================
# 🔢 OTP Model
# ==========================================================
class OTP(models.Model):
    phone = models.CharField(max_length=20)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phone} - {self.code}"

    class Meta:
        verbose_name = "رمز تحقق"
        verbose_name_plural = "أكواد التحقق"
