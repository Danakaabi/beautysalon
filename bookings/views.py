from django.contrib import messages
from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404, redirect, render

from catalog.models import Service
from scheduling.models import Staff, StaffService
from .models import Booking, BookingItem, TimeSlot


ACTIVE_BOOKING_STATUSES = ["pending", "confirmed"]


def _get_selected_service(service_data):
    if not service_data:
        return None

    service_id = service_data.get("id")

    if service_id:
        return Service.objects.filter(id=service_id, is_active=True).first()

    return Service.objects.filter(
        name=service_data.get("name"),
        is_active=True,
    ).first()


def select_service_view(request):
    services = Service.objects.filter(is_active=True).select_related("category")

    if request.method == "POST":
        service_value = request.POST.get("service", "").strip()

        if not service_value:
            messages.error(request, "يرجى اختيار الخدمة.")
            return redirect("bookings:select_service")

        selected_service = None

        if service_value.isdigit():
            selected_service = services.filter(id=int(service_value)).first()

        if not selected_service:
            messages.error(request, "الخدمة المحددة غير متاحة.")
            return redirect("bookings:select_service")

        request.session["service"] = {
            "id": selected_service.id,
            "name": selected_service.name,
            "price": str(selected_service.price),
            "duration_minutes": selected_service.duration_minutes,
        }

        for key in ("selected_staff_id", "selected_staff_name", "selected_date", "selected_time"):
            request.session.pop(key, None)

        return redirect("bookings:select_date_time")

    return render(request, "services.html", {"services": services})

def select_date_time_view(request):
    service_data = request.session.get("service")

    if not service_data:
        messages.error(request, "يرجى اختيار الخدمة أولاً.")
        return redirect("bookings:select_service")

    service_obj = _get_selected_service(service_data)

    staff_members = (
        Staff.objects
        .filter(is_active=True, services__service=service_obj)
        .distinct()
        .order_by("name")
        if service_obj else Staff.objects.filter(is_active=True).order_by("name")
    )

    selected_date = request.GET.get("date", "").strip()
    selected_staff_id = request.GET.get("staff_id", "auto").strip()

    if request.method == "POST":
        selected_date = request.POST.get("date", "").strip()
        selected_staff_id = request.POST.get("staff_id", "auto").strip()
        time_str = request.POST.get("time", "").strip()

        if not selected_date or not time_str:
            messages.error(request, "يرجى اختيار التاريخ والوقت.")
            return redirect("bookings:select_date_time")

        request.session["selected_date"] = selected_date
        request.session["selected_time"] = time_str

        if selected_staff_id == "auto":
            request.session["selected_staff_id"] = None
            request.session["selected_staff_name"] = "أي موظفة متاحة"
        else:
            selected_staff = Staff.objects.filter(id=selected_staff_id, is_active=True).first()

            if not selected_staff:
                messages.error(request, "الموظفة المحددة غير متاحة.")
                return redirect("bookings:select_date_time")

            request.session["selected_staff_id"] = selected_staff.id
            request.session["selected_staff_name"] = selected_staff.name

        return redirect("bookings:confirm_booking")

    booked_time_ids = set()

    if selected_date and selected_staff_id != "auto":
        booked_time_ids = set(
            Booking.objects.filter(
                date=selected_date,
                staff_member_id=selected_staff_id,
                status__in=ACTIVE_BOOKING_STATUSES,
            ).values_list("time_id", flat=True)
        )

    time_slots = [
        {
            "time": slot.time,
            "is_booked": slot.id in booked_time_ids,
        }
        for slot in TimeSlot.objects.all().order_by("time")
    ]

    return render(
        request,
        "booking_date_time.html",
        {
            "staff_members": staff_members,
            "time_slots": time_slots,
            "selected_date": selected_date,
            "selected_staff_id": selected_staff_id,
        },
    )


def confirm_booking_view(request):
    service_data = request.session.get("service")
    date_val = request.session.get("selected_date")
    time_str = request.session.get("selected_time")
    staff_name = request.session.get("selected_staff_name", "أي موظفة متاحة")

    if not service_data or not date_val or not time_str:
        messages.error(request, "الرجاء اختيار الخدمة والتاريخ والوقت.")
        return redirect("bookings:select_service")

    return render(
        request,
        "confirm.html",
        {
            "service": service_data.get("name", "بدون تفصيل"),
            "service_price": service_data.get("price", "0.00"),
            "staff_name": staff_name,
            "date": date_val,
            "time": time_str,
            "customer_phone": request.user.phone if request.user.is_authenticated else "غير مسجل",
        },
    )


@transaction.atomic
def complete_booking_view(request):
    if request.method != "POST":
        return redirect("bookings:select_service")

    if not request.user.is_authenticated:
        messages.error(request, "يجب تسجيل الدخول.")
        return redirect("accounts:login_page")

    service_data = request.session.get("service")
    date_val = request.session.get("selected_date")
    time_str = request.session.get("selected_time")
    selected_staff_id = request.session.get("selected_staff_id")

    if not service_data or not date_val or not time_str:
        messages.error(request, "حدث خطأ.. يرجى إعادة العملية.")
        return redirect("bookings:select_service")

    slot = TimeSlot.objects.filter(time=time_str).first()

    if not slot:
        messages.error(request, "الوقت المحدد غير موجود.")
        return redirect("bookings:select_date_time")

    service_obj = _get_selected_service(service_data)

    staff_member = None

    if selected_staff_id:
        staff_member = Staff.objects.filter(id=selected_staff_id, is_active=True).first()

        if not staff_member:
            messages.error(request, "الموظفة المحددة غير متاحة.")
            return redirect("bookings:select_date_time")

        if service_obj and not StaffService.objects.filter(staff=staff_member, service=service_obj).exists():
            messages.error(request, "الموظفة المحددة لا تقدم هذه الخدمة.")
            return redirect("bookings:select_date_time")
    else:
        busy_staff_ids = Booking.objects.filter(
            date=date_val,
            time=slot,
            status__in=ACTIVE_BOOKING_STATUSES,
        ).values_list("staff_member_id", flat=True)

        if service_obj:
            staff_service = (
                StaffService.objects
                .filter(service=service_obj, staff__is_active=True)
                .exclude(staff_id__in=busy_staff_ids)
                .select_related("staff")
                .order_by("staff__name")
                .first()
            )

            if staff_service:
                staff_member = staff_service.staff

        if not staff_member:
            staff_member = (
                Staff.objects
                .filter(is_active=True)
                .exclude(id__in=busy_staff_ids)
                .order_by("name")
                .first()
            )

    if not staff_member:
        messages.error(request, "لا توجد موظفة متاحة في هذا الوقت.")
        return redirect("bookings:select_date_time")

    if Booking.objects.filter(
        date=date_val,
        time=slot,
        staff_member=staff_member,
        status__in=ACTIVE_BOOKING_STATUSES,
    ).exists():
        messages.error(request, "هذا الموعد محجوز مسبقاً لهذه الموظفة.")
        return redirect("bookings:select_date_time")

    try:
        booking = Booking.objects.create(
            user=request.user,
            service=service_data.get("name", ""),
            date=date_val,
            time=slot,
            staff_member=staff_member,
            status="confirmed",
            total_amount=0,
        )
    except IntegrityError:
        messages.error(request, "هذا الموعد محجوز مسبقاً.")
        return redirect("bookings:select_date_time")

    if service_obj:
        BookingItem.objects.create(
            booking=booking,
            service=service_obj,
            price_at_booking=service_obj.price,
            duration_at_booking=service_obj.duration_minutes,
        )
        booking.recalculate_total()

    for key in (
        "service",
        "selected_date",
        "selected_time",
        "selected_staff_id",
        "selected_staff_name",
        "edit_booking_id",
    ):
        request.session.pop(key, None)

    return redirect("bookings:booking_success")


def booking_success_view(request):
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


def my_bookings_view(request):
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


def cancel_booking(request, booking_id):
    if not request.user.is_authenticated:
        return redirect("accounts:login_page")

    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if booking.status == "canceled":
        messages.info(request, "الحجز ملغي مسبقاً.")
        return redirect("accounts:dashboard")

    booking.status = "canceled"
    booking.save(update_fields=["status", "updated_at"])

    messages.success(request, "تم إلغاء الحجز بنجاح.")
    return redirect("accounts:dashboard")


def edit_booking(request, booking_id):
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

    request.session["selected_staff_id"] = booking.staff_member.id if booking.staff_member else None
    request.session["selected_staff_name"] = booking.staff_member.name if booking.staff_member else "أي موظفة متاحة"
    request.session["edit_booking_id"] = booking.id

    return redirect("bookings:select_date_time")