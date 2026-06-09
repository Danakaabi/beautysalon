# accounts/views.py

import json
import re
from datetime import date

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from bookings.models import Booking
from .models import CustomUser, OTP
from .services import generate_otp, verify_otp


PHONE_PATTERN = re.compile(r"^05\d{8}$")

# الحالات التي تعتبر حجزًا قادمًا فعّالًا
ACTIVE_BOOKING_STATUSES = ["pending", "confirmed"]


def is_valid_saudi_phone(phone: str) -> bool:
    """التحقق من رقم جوال سعودي بصيغة 05xxxxxxxx."""
    return bool(phone and PHONE_PATTERN.match(phone.strip()))


# ==========================================================
# صفحة تسجيل الدخول
# ==========================================================
def login_page(request):
    """عرض صفحة إدخال رقم الجوال."""
    return render(request, "login.html")


# ==========================================================
# صفحة إدخال رمز OTP
# ==========================================================
def otp_verify_view(request):
    """عرض صفحة إدخال رمز التحقق."""
    phone = request.GET.get("phone", "").strip()
    return render(request, "otp_verify.html", {"phone": phone})


# ==========================================================
# إرسال كود OTP
# ==========================================================
@csrf_exempt
@require_http_methods(["POST"])
def send_otp(request):
    """إرسال رمز التحقق إلى رقم الجوال."""
    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"error": "صيغة JSON غير صحيحة"}, status=400)

    phone = str(data.get("phone", "")).strip()

    if not is_valid_saudi_phone(phone):
        return JsonResponse({"error": "رقم الجوال غير صحيح"}, status=400)

    otp = generate_otp(phone)

    response = {"message": "تم إرسال كود التحقق"}

    # يظهر فقط أثناء التطوير
    if settings.DEBUG:
        response["otp_debug"] = otp

    return JsonResponse(response, status=200)


# ==========================================================
# التحقق من الكود + تسجيل الدخول
# ==========================================================
@csrf_exempt
@require_http_methods(["POST"])
def verify_and_login(request):
    """التحقق من كود OTP وتسجيل دخول المستخدم."""
    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"error": "صيغة JSON غير صحيحة"}, status=400)

    phone = str(data.get("phone", "")).strip()
    code = str(data.get("code", "")).strip()

    if not is_valid_saudi_phone(phone):
        return JsonResponse({"error": "رقم الجوال غير صحيح"}, status=400)

    if not code:
        return JsonResponse({"error": "كود التحقق مطلوب"}, status=400)

    if not verify_otp(phone, code):
        return JsonResponse({"error": "الكود غير صحيح أو منتهي"}, status=400)

    user, created = CustomUser.objects.get_or_create(phone=phone)

    login(request, user)
    request.session["customer_phone"] = user.phone

    return JsonResponse(
        {
            "message": "تم تسجيل الدخول بنجاح",
            "new_user": created,
            "redirect": "/accounts/dashboard/",
        },
        status=200,
    )


# ==========================================================
# لوحة العميل
# ==========================================================
def customer_dashboard(request):
    """
    لوحة العميل:
    - تعرض أقرب حجز قادم فقط إذا كان pending أو confirmed.
    - تعرض الحجوزات السابقة أو الملغية أو المكتملة في قسم الحجوزات السابقة.
    """
    if not request.user.is_authenticated:
        return redirect("accounts:login_page")

    today = date.today()

    # QuerySet أساسي مع تحسين الأداء
    bookings = (
        Booking.objects
        .filter(user=request.user)
        .select_related("time", "staff_member")
        .prefetch_related("items__service")
    )

    # الحجز القادم: لا نعرض الملغي أو المكتمل هنا
    upcoming_booking = (
        bookings
        .filter(
            date__gte=today,
            status__in=ACTIVE_BOOKING_STATUSES,
        )
        .order_by("date", "time__time")
        .first()
    )

    # الحجوزات السابقة:
    # 1) حجوزات تاريخها قديم
    # 2) أو حجوزات ملغية / مكتملة / لم يحضر
    previous_bookings = (
        bookings
        .exclude(id=upcoming_booking.id if upcoming_booking else None)
        .filter(
            status__in=["canceled", "completed", "no_show"]
        )
        .order_by("-date", "-created_at")
    )

    old_bookings = (
        bookings
        .filter(date__lt=today)
        .exclude(status__in=["canceled", "completed", "no_show"])
        .order_by("-date", "-created_at")
    )

    # ندمجهم في قائمة واحدة حتى تظهر كل الحجوزات السابقة والمنتهية
    previous_bookings = list(previous_bookings) + list(old_bookings)

    return render(
        request,
        "dashboard.html",
        {
            "phone": request.user.phone,
            "upcoming_booking": upcoming_booking,
            "previous_bookings": previous_bookings,
        },
    )


# ==========================================================
# صفحة قائمة الخدمات
# ==========================================================
def services_page(request):
    """عرض صفحة الخدمات."""
    return render(request, "services.html")


# ==========================================================
# صفحة تواصل معنا
# ==========================================================
@require_http_methods(["GET", "POST"])
def contact_page(request):
    """
    صفحة تواصل معنا.
    حالياً لا يوجد ContactMessage model.
    """
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        phone = request.POST.get("phone", "").strip()
        message_text = request.POST.get("message", "").strip()

        if not name or not phone or not message_text:
            messages.error(request, "يرجى تعبئة جميع الحقول.")
            return redirect("accounts:contact")

        if not is_valid_saudi_phone(phone):
            messages.error(request, "رقم الجوال غير صحيح.")
            return redirect("accounts:contact")

        # مؤقتاً للتطوير فقط
        if settings.DEBUG:
            print("Contact Message:")
            print("Name:", name)
            print("Phone:", phone)
            print("Message:", message_text)

        messages.success(request, "تم إرسال رسالتك بنجاح.")
        return redirect("accounts:contact")

    return render(request, "contact.html")


# ==========================================================
# DEV ONLY: عرض آخر OTP للتجربة فقط
# ==========================================================
def dev_last_otp(request):
    """
    عرض آخر كود OTP أثناء التطوير فقط.
    لا يعمل في الإنتاج إذا DEBUG=False.
    """
    if not settings.DEBUG:
        return JsonResponse({"error": "غير متاح"}, status=403)

    phone = request.GET.get("phone", "").strip()

    otps = OTP.objects.all().order_by("-created_at")

    if phone:
        otps = otps.filter(phone=phone)

    latest_otp = otps.first()

    if not latest_otp:
        return JsonResponse(
            {"otp": None, "message": "لا يوجد OTP محفوظ"},
            status=404,
        )

    return JsonResponse(
        {
            "phone": latest_otp.phone,
            "code": latest_otp.code,
            "created_at": latest_otp.created_at.isoformat(),
        }
    )