from django.db import models

from accounts.models import CustomUser
from catalog.models import Service


class Staff(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="staff_profile",
        verbose_name="اسم المستخدم",
    )

    name = models.CharField(
        max_length=100,
        verbose_name="اسم الموظفة",
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="رقم الجوال",
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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "موظفة"
        verbose_name_plural = "الموظفات"
        ordering = ["name"]


class StaffService(models.Model):
    staff = models.ForeignKey(
        Staff,
        on_delete=models.CASCADE,
        related_name="services",
        verbose_name="الموظفة",
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="staff_members",
        verbose_name="الخدمة",
    )

    def __str__(self):
        return f"{self.staff.name} - {self.service.name}"

    class Meta:
        verbose_name = "خدمة الموظفة"
        verbose_name_plural = "خدمات الموظفات"
        constraints = [
            models.UniqueConstraint(
                fields=["staff", "service"],
                name="unique_staff_service",
            ),
        ]


class StaffAvailability(models.Model):
    DAYS_OF_WEEK = [
        ("saturday", "السبت"),
        ("sunday", "الأحد"),
        ("monday", "الإثنين"),
        ("tuesday", "الثلاثاء"),
        ("wednesday", "الأربعاء"),
        ("thursday", "الخميس"),
        ("friday", "الجمعة"),
    ]

    staff = models.ForeignKey(
        Staff,
        on_delete=models.CASCADE,
        related_name="availabilities",
        verbose_name="الموظفة",
    )

    day_of_week = models.CharField(
        max_length=20,
        choices=DAYS_OF_WEEK,
        verbose_name="اليوم",
    )

    start_time = models.TimeField(
        verbose_name="وقت بداية العمل",
    )

    end_time = models.TimeField(
        verbose_name="وقت نهاية العمل",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="متاحة للحجز",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاريخ الإنشاء",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="آخر تحديث",
    )

    def __str__(self):
        return (
            f"{self.staff.name} - "
            f"{self.get_day_of_week_display()} "
            f"من {self.start_time} إلى {self.end_time}"
        )

    class Meta:
        verbose_name = "توفر الموظفة"
        verbose_name_plural = "توفر الموظفات"
        ordering = [
            "staff",
            "day_of_week",
            "start_time",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=["staff", "day_of_week"],
                name="unique_staff_availability_per_day",
            ),
            
        ]