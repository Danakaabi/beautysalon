from django.core.validators import MinValueValidator
from django.db import models


class ServiceCategory(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="اسم التصنيف",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="الوصف",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="نشط",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاريخ الإنشاء",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="آخر تحديث",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "تصنيف خدمة"
        verbose_name_plural = "تصنيفات الخدمات"

    def __str__(self):
        return self.name


class Service(models.Model):
    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="services",
        verbose_name="التصنيف",
    )

    name = models.CharField(
        max_length=120,
        verbose_name="اسم الخدمة",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="وصف الخدمة",
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="السعر",
    )
    duration_minutes = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="مدة الخدمة بالدقائق",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="نشطة",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاريخ الإنشاء",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="آخر تحديث",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "خدمة"
        verbose_name_plural = "الخدمات"
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["is_active"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["category", "name"],
                name="unique_service_name_per_category",
            )
        ]

    def __str__(self):
        return self.name