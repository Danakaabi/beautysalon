from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from bookings.models import Booking
from .models import Staff, StaffService


# ============================
# Staff Access Helpers
# ============================

def get_staff_profile(user):
    """
    إرجاع ملف الموظفة المرتبط بالمستخدم.
    نستخدم getattr حتى لا يحدث خطأ إذا لم يكن للمستخدم staff_profile.
    """
    return getattr(user, "staff_profile", None)


def staff_required(request):
    """
    حماية صفحات الموظفة:
    - المستخدم مسجل دخول
    - دوره staff أو admin
    - لديه Staff Profile مرتبط
    """
    return (
        request.user.is_authenticated
        and getattr(request.user, "role", None) == "staff"
        and get_staff_profile(request.user) is not None
    )


def deny_staff_access(request):
    """
    إعادة المستخدم غير المصرح له إلى صفحة العميل الرئيسية.
    """
    messages.error(
        request,
        "لا تملكين صلاحية الدخول إلى بوابة الموظفة."
    )
    return redirect("portal_client:home")


# ============================
# Staff Dashboard
# ============================

@login_required
def staff_dashboard(request):
    if not staff_required(request):
        return deny_staff_access(request)

    staff = get_staff_profile(request.user)
    today = timezone.localdate()

    today_bookings = (
        Booking.objects
        .filter(
            staff_member=staff,
            date=today,
        )
        .exclude(status="canceled")
        .select_related("user", "time")
        .order_by("time__time")
    )

    context = {
        "staff": staff,
        "today_bookings": today_bookings,
        "total_today": today_bookings.count(),
    }

    return render(request, "staff/dashboard.html", context)


# ============================
# Staff Bookings
# ============================

@login_required
def staff_bookings(request):
    if not staff_required(request):
        return deny_staff_access(request)

    staff = get_staff_profile(request.user)

    bookings = (
        Booking.objects
        .filter(staff_member=staff)
        .select_related("user", "time", "staff_member")
        .prefetch_related("items__service")
        .order_by("-date", "-created_at")
    )

    return render(
        request,
        "staff/bookings.html",
        {
            "staff": staff,
            "bookings": bookings,
        },
    )


# ============================
# Staff Schedule
# ============================

@login_required
def staff_schedule(request):
    if not staff_required(request):
        return deny_staff_access(request)

    staff = get_staff_profile(request.user)
    today = timezone.localdate()

    schedule = (
        Booking.objects
        .filter(
            staff_member=staff,
            date=today,
        )
        .exclude(status="canceled")
        .select_related("user", "time", "staff_member")
        .prefetch_related("items__service")
        .order_by("time__time")
    )

    return render(
        request,
        "staff/schedule.html",
        {
            "staff": staff,
            "schedule": schedule,
            "today": today,
        },
    )


# ============================
# Staff Profile
# ============================

@login_required
def staff_profile(request):
    if not staff_required(request):
        return deny_staff_access(request)

    staff = get_staff_profile(request.user)
    today = timezone.localdate()

    total_bookings = Booking.objects.filter(
        staff_member=staff
    ).count()

    completed_bookings = Booking.objects.filter(
        staff_member=staff,
        status="completed",
    ).count()

    upcoming_bookings = (
        Booking.objects
        .filter(
            staff_member=staff,
            date__gte=today,
        )
        .exclude(status__in=["completed", "canceled", "no_show"])
        .count()
    )

    services = (
        StaffService.objects
        .filter(
            staff=staff,
            is_active=True,
        )
        .select_related("service")
        .order_by("service__name")
    )

    return render(
        request,
        "staff/profile.html",
        {
            "staff": staff,
            "total_bookings": total_bookings,
            "completed_bookings": completed_bookings,
            "upcoming_bookings": upcoming_bookings,
            "services": services,
        },
    )


# ============================
# Staff Notifications
# ============================

@login_required
def staff_notifications(request):
    if not staff_required(request):
        return deny_staff_access(request)

    staff = get_staff_profile(request.user)

    return render(
        request,
        "staff/notifications.html",
        {
            "staff": staff,
        },
    )


# ============================
# Booking Detail
# ============================

@login_required
def booking_detail(request, booking_id):
    if not staff_required(request):
        return deny_staff_access(request)

    staff = get_staff_profile(request.user)

    booking = get_object_or_404(
        Booking.objects
        .select_related("user", "staff_member", "time")
        .prefetch_related("items__service"),
        pk=booking_id,
        staff_member=staff,
    )

    return render(
        request,
        "staff/booking-detail.html",
        {
            "staff": staff,
            "booking": booking,
        },
    )

@login_required
def start_booking_service(request, booking_id):
    if not staff_required(request):
        return deny_staff_access(request)

    staff = get_staff_profile(request.user)

    booking = get_object_or_404(
        Booking,
        pk=booking_id,
        staff_member=staff,
        status="confirmed",
    )

    booking.status = "in_progress"
    booking.save(update_fields=["status", "updated_at"])

    messages.success(request, "تم بدء الخدمة بنجاح.")
    return redirect("scheduling:staff_bookings")

# ============================
# Complete Booking Service
# ============================
@login_required
def complete_booking_service(request, booking_id):
    if not staff_required(request):
        return deny_staff_access(request)

    staff = get_staff_profile(request.user)

    booking = get_object_or_404(
        Booking,
        pk=booking_id,
        staff_member=staff,
        status="in_progress",
    )

    booking.status = "completed"
    booking.save(update_fields=["status", "updated_at"])

    messages.success(request, "تم إنهاء الخدمة بنجاح.")
    return redirect("scheduling:staff_bookings")