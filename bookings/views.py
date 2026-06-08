from datetime import date

from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from catalog.models import Service
from .models import Booking, BookingItem, TimeSlot


# ============================================================
# 1) اختيار الخدمة
# ============================================================
def select_service_view(request):
    """الخطوة الأولى: اختيار الخدمة."""

    services = Service.objects.filter(is_active=True).select_related("category")

    if request.method == "POST":
        service_value = request.POST.get("service", "").strip()

        if not service_value:
            messages.error(request, "يرجى اختيار الخدمة.")
            return redirect("bookings:select_service")

        selected_service = None

        if service_value.isdigit():
            selected_service = services.filter(id=int(service_value)).first()

        if selected_service:
            request.session["service"] = {
                "id": selected_service.id,
                "name": selected_service.name,
                "price": str(selected_service.price),
                "duration_minutes": selected_service.duration_minutes,
            }
        else:
            # دعم مؤقت للخدمات القديمة المكتوبة كنص داخل HTML
            request.session["service"] = {
                "id": None,
                "name": service_value,
                "price": "0.00",
                "duration_minutes": 0,
            }

        return redirect("bookings:select_date_time")

    return render(request, "services.html", {"services": services})


# ============================================================
# 2) اختيار التاريخ والوقت
# ============================================================
def select_date_time_view(request):
    """الخطوة الثانية: اختيار تاريخ ووقت الموعد."""

    if not request.session.get("service"):
        messages.error(request, "يرجى اختيار الخدمة أولاً.")
        return redirect("bookings:select_service")

    times = TimeSlot.objects.all().order_by("time")

    if request.method == "POST":
        date_val = request.POST.get("date", "").strip()
        time_str = request.POST.get("time", "").strip()

        if not date_val or not time_str:
            messages.error(request, "يرجى اختيار التاريخ والوقت.")
            return redirect("bookings:select_date_time")

        request.session["selected_date"] = date_val
        request.session["selected_time"] = time_str

        return redirect("bookings:confirm_booking")

    return render(request, "booking_date_time.html", {"times": times})


# ============================================================
# 3) شاشة تأكيد تفاصيل الموعد
# ============================================================
def confirm_booking_view(request):
    """عرض التفاصيل بعد اختيار التاريخ والوقت."""

    service = request.session.get("service")
    date_val = request.session.get("selected_date")
    time_str = request.session.get("selected_time")

    if not service or not date_val or not time_str:
        messages.error(request, "الرجاء اختيار الخدمة والتاريخ والوقت.")
        return redirect("bookings:select_service")

    return render(
        request,
        "confirm.html",
        {
            "service": service.get("name"),
            "date": date_val,
            "time": time_str,
            "customer_phone": request.user.phone if request.user.is_authenticated else "غير مسجل",
        },
    )


# ============================================================
# 4) إنشاء الحجز فعلياً
# ============================================================
@transaction.atomic
def complete_booking_view(request):
    """الخطوة الأخيرة: إنشاء الحجز."""

    if not request.user.is_authenticated:
        messages.error(request, "يجب تسجيل الدخول.")
        return redirect("accounts:login_page")

    service_data = request.session.get("service")
    date_val = request.session.get("selected_date")
    time_str = request.session.get("selected_time")

    if not service_data or not date_val or not time_str:
        messages.error(request, "حدث خطأ.. يرجى إعادة العملية.")
        return redirect("bookings:select_service")

    slot = TimeSlot.objects.filter(time=time_str).first()
    if not slot:
        messages.error(request, "الوقت المحدد غير موجود.")
        return redirect("bookings:select_date_time")

    service_obj = None
    service_id = service_data.get("id")

    if service_id:
        service_obj = Service.objects.filter(id=service_id, is_active=True).first()

    # إنشاء الحجز الأساسي
    booking = Booking.objects.create(
        user=request.user,
        service=service_data.get("name", ""),
        date=date_val,
        time=slot,
        status="confirmed",
        total_amount=0,
    )

    # إنشاء BookingItem إذا كانت الخدمة موجودة في قاعدة البيانات
    if service_obj:
        BookingItem.objects.create(
            booking=booking,
            service=service_obj,
            price_at_booking=service_obj.price,
            duration_at_booking=service_obj.duration_minutes,
        )
        booking.recalculate_total()

    for key in ("service", "selected_date", "selected_time", "edit_booking_id"):
        request.session.pop(key, None)

    return redirect("bookings:booking_success")


# ============================================================
# 5) صفحة نجاح الحجز
# ============================================================
def booking_success_view(request):
    """عرض آخر حجز للعميل."""

    latest_booking = None

    if request.user.is_authenticated:
        latest_booking = (
            Booking.objects
            .filter(user=request.user)
            .select_related("time", "staff_member")
            .prefetch_related("items__service")
            .order_by("-created_at")
            .first()
        )

    return render(request, "booking_success.html", {"booking": latest_booking})


# ============================================================
# 6) صفحة جميع الحجوزات
# ============================================================
def my_bookings_view(request):
    """عرض جميع حجوزات العميل."""

    if not request.user.is_authenticated:
        return redirect("accounts:login_page")

    bookings = (
        Booking.objects
        .filter(user=request.user)
        .select_related("time", "staff_member")
        .prefetch_related("items__service")
        .order_by("-created_at")
    )

    return render(request, "my_bookings.html", {"bookings": bookings})


# ============================================================
# 7) إلغاء الحجز
# ============================================================
def cancel_booking(request, booking_id):
    """إلغاء حجز معين."""

    if not request.user.is_authenticated:
        return redirect("accounts:login_page")

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user,
    )

    if booking.status == "canceled":
        messages.info(request, "الحجز ملغي مسبقاً.")
        return redirect("accounts:dashboard")

    booking.status = "canceled"
    booking.save(update_fields=["status", "updated_at"])

    messages.success(request, "تم إلغاء الحجز بنجاح.")
    return redirect("accounts:dashboard")


# ============================================================
# 8) تعديل الموعد
# ============================================================
def edit_booking(request, booking_id):
    """إعادة العميل لاختيار التاريخ عند تعديل الموعد."""

    if not request.user.is_authenticated:
        return redirect("accounts:login_page")

    booking = get_object_or_404(
        Booking.objects.prefetch_related("items__service"),
        id=booking_id,
        user=request.user,
    )

    first_item = booking.items.first()

    if first_item:
        request.session["service"] = {
            "id": first_item.service.id,
            "name": first_item.service.name,
            "price": str(first_item.price_at_booking),
            "duration_minutes": first_item.duration_at_booking,
        }
    else:
        request.session["service"] = {
            "id": None,
            "name": booking.service,
            "price": "0.00",
            "duration_minutes": 0,
        }

    request.session["edit_booking_id"] = booking.id

    return redirect("bookings:select_date_time")