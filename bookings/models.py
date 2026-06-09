from django.core.validators import MinValueValidator
from django.db import models

from accounts.models import CustomUser
from catalog.models import Service
from scheduling.models import Staff


class TimeSlot(models.Model):
    time = models.TimeField(verbose_name="الوقت")

    class Meta:
        ordering = ["time"]
        verbose_name = "وقت متاح"
        verbose_name_plural = "الأوقات المتاحة"

    def __str__(self):
        return self.time.strftime("%H:%M")


class Booking(models.Model):
    STATUS_CHOICES = [
        ("pending", "قيد الانتظار"),
        ("confirmed", "مؤكد"),
        ("completed", "مكتمل"),
        ("canceled", "ملغي"),
        ("no_show", "لم يحضر"),
    ]

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="bookings",
        verbose_name="العميل",
    )

    # Legacy field من V1 — نُبقيه مؤقتاً حتى لا نكسر الحجز القديم
    service = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="اسم الخدمة القديم",
        help_text="حقل قديم من V1. الخدمات الجديدة تحفظ في BookingItem.",
    )

    date = models.DateField(verbose_name="تاريخ الحجز")

    time = models.ForeignKey(
        TimeSlot,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bookings",
        verbose_name="الوقت",
    )

    # Legacy field من V1
    staff = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="اسم الموظفة القديم",
        help_text="حقل قديم من V1.",
    )

    staff_member = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bookings",
        verbose_name="الموظفة",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="confirmed",
        verbose_name="حالة الحجز",
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="إجمالي السعر",
    )

    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name="ملاحظات",
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
        ordering = ["-created_at"]
        verbose_name = "حجز"
        verbose_name_plural = "الحجوزات"
        indexes = [
            models.Index(fields=["date", "time"]),
            models.Index(fields=["status"]),
            models.Index(fields=["staff_member", "date"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["date", "time", "staff_member"],
                condition=models.Q(status__in=["pending", "confirmed"]),
                name="unique_active_booking_per_staff_time",
            )
        ]
    def __str__(self):
        user_phone = getattr(self.user, "phone", "بدون رقم")
        time_display = self.time.time.strftime("%H:%M") if self.time else "—"
        return f"{user_phone} | {self.date} - {time_display}"

    def recalculate_total(self):
        total = sum(item.price_at_booking for item in self.items.all())
        self.total_amount = total
        self.save(update_fields=["total_amount", "updated_at"])
        return total


class BookingItem(models.Model):
    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="الحجز",
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.PROTECT,
        related_name="booking_items",
        verbose_name="الخدمة",
    )

    price_at_booking = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="السعر وقت الحجز",
    )

    duration_at_booking = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="المدة وقت الحجز بالدقائق",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاريخ الإضافة",
    )

    class Meta:
        ordering = ["id"]
        verbose_name = "خدمة داخل الحجز"
        verbose_name_plural = "الخدمات داخل الحجز"
        constraints = [
            models.UniqueConstraint(
                fields=["booking", "service"],
                name="unique_service_per_booking",
            )
        ]

    def __str__(self):
        return f"{self.booking} | {self.service}"