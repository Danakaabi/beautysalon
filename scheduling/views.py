# scheduling/views.py

from django.contrib.auth.decorators import login_required
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
    staff = getattr(request.user, "staff_profile", None)

    today = timezone.localdate()

    schedule = Booking.objects.filter(
        staff_member=staff,
        date=today,
    ).select_related(
        "user",
        "time",
    )

    return render(
        request,
        "staff/schedule.html",
        {
            "schedule": schedule,
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