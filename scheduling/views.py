# scheduling/views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render
from django.utils import timezone

from bookings.models import Booking
from .models import Staff


@login_required
def staff_dashboard(request):
    staff = getattr(request.user, "staff_profile", None)

    if not staff:
        return render(
            request,
            "staff/dashboard.html",
            {
                "error": "لا يوجد ملف موظفة مرتبط بهذا الحساب"
            }
        )

    today = timezone.localdate()

    today_bookings = Booking.objects.filter(
        staff_member=staff,
        date=today
    ).select_related("user", "time")

    context = {
        "staff": staff,
        "today_bookings": today_bookings,
        "total_today": today_bookings.count(),
    }

    return render(
        request,
        "staff/dashboard.html",
        context,
    )


@login_required
def staff_bookings(request):
    staff = getattr(request.user, "staff_profile", None)

    bookings = Booking.objects.filter(
        staff_member=staff
    ).select_related(
        "user",
        "time"
    ).order_by("-date")

    return render(
        request,
        "staff/bookings.html",
        {
            "bookings": bookings,
        },
    )


@login_required
def staff_schedule(request):
    today = timezone.localdate()

    staff = getattr(request.user, "staff_profile", None)

    # دعم الوضع الحالي للمشروع حيث Staff غير مربوط بـ User
    if not staff:
        user_phone = getattr(request.user, "phone", None)

        if user_phone:
            staff = Staff.objects.filter(
                phone=user_phone,
                is_active=True,
            ).first()

    schedule = (
        Booking.objects
        .filter(
            date=today,
        )
        .exclude(
            status="canceled",
        )
        .select_related(
            "user",
            "time",
            "staff_member",
        )
        .prefetch_related(
            "items__service",
        )
        .order_by(
            "time__time",
        )
    )

    # إذا تم العثور على موظفة مرتبطة بالحساب
    # نعرض مواعيدها فقط
    if staff:
        schedule = schedule.filter(
            staff_member=staff,
        )

    return render(
        request,
        "staff/schedule.html",
        {
            "schedule": schedule,
            "today": today,
            "staff": staff,
        },
    )


@login_required
def staff_profile(request):
    staff = getattr(request.user, "staff_profile", None)

    return render(
        request,
        "staff/profile.html",
        {
            "staff": staff,
        },
    )


@login_required
def staff_notifications(request):
    return render(
        request,
        "staff/notifications.html",
    )
@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(
        Booking.objects
        .select_related(
            "user",
            "staff_member",
            "time",
        )
        .prefetch_related(
            "items__service",
        ),
        pk=booking_id,
    )

    return render(
        request,
        "staff/booking-detail.html",
        {
            "booking": booking,
        },
    )