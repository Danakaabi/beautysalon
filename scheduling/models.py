from django.db import models


class Staff(models.Model):
    full_name = models.CharField(
        max_length=150,
        verbose_name="الاسم الكامل"
    )

    phone = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="رقم الجوال"
    )

    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name="البريد الإلكتروني"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="نشطة"
    )

    hire_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="تاريخ التوظيف"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["full_name"]
        verbose_name = "موظفة"
        verbose_name_plural = "الموظفات"

    def __str__(self):
        return self.full_name
    

from catalog.models import Service


class StaffService(models.Model):
    staff = models.ForeignKey(
        Staff,
        on_delete=models.CASCADE,
        related_name="staff_services"
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="service_staff"
    )

    class Meta:
        verbose_name = "خدمة موظفة"
        verbose_name_plural = "خدمات الموظفات"

        constraints = [
            models.UniqueConstraint(
                fields=["staff", "service"],
                name="unique_staff_service"
            )
        ]

    def __str__(self):
        return f"{self.staff} - {self.service}"