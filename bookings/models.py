from django.db import models
from accounts.models import CustomUser


class TimeSlot(models.Model):
    """
    يمثل وقتاً متاحاً يمكن للزبونة اختياره (مثل 10:00 ص أو 6:30 م)
    """
    time = models.TimeField()

    class Meta:
        ordering = ["time"]
        verbose_name = "وقت متاح"
        verbose_name_plural = "الأوقات المتاحة"

    def __str__(self):
        return self.time.strftime("%H:%M")


class Booking(models.Model):
    """
    نموذج الحجز:
    - المستخدم
    - الخدمة
    - التاريخ
    - الوقت
    - الموظفة (اختياري)
    - حالة الحجز
    """

    STATUS_CHOICES = [
        ("pending", "قيد الانتظار"),
        ("confirmed", "مؤكد"),
        ("completed", "مكتمل"),
        ("canceled", "ملغي"),
    ]

    # المستخدم الذي قام بالحجز
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    # اسم الخدمة
    service = models.CharField(max_length=200)

    # التاريخ
    date = models.DateField()

    # الوقت من جدول TimeSlot
    time = models.ForeignKey(
        TimeSlot,
        on_delete=models.SET_NULL,
        null=True,
        related_name="bookings"
    )

    # الموظفة (اختياري)
    staff = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="اسم الموظفة (اختياري)"
    )

    # حالة الحجز
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="confirmed"
    )

    # تاريخ إنشاء الحجز
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "حجز"
        verbose_name_plural = "الحجوزات"

    def __str__(self):
        user_phone = getattr(self.user, "phone", "بدون رقم")
        time_display = self.time.time.strftime("%H:%M") if self.time else "—"
        return f"{user_phone} | {self.service} | {self.date} - {time_display}"
