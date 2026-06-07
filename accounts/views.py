# accounts/views.py

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login
from datetime import date
import json

from .models import CustomUser
from .services import generate_otp, verify_otp
from bookings.models import Booking   # ⬅ أهم سطر — لإظهار الحجوزات


# ==========================================================
# 📌 صفحة تسجيل الدخول
# ==========================================================
def login_page(request):
    """عرض صفحة إدخال رقم الجوال"""
    return render(request, "login.html")


# ==========================================================
# 📌 صفحة إدخال رمز OTP
# ==========================================================
def otp_verify_view(request):
    """عرض صفحة إدخال رمز التحقق"""
    phone = request.GET.get("phone", "")
    return render(request, "otp_verify.html", {"phone": phone})


# ==========================================================
# 📌 إرسال كود OTP
# ==========================================================
@csrf_exempt
def send_otp(request):
    """إرسال رمز التحقق إلى رقم الجوال"""
    if request.method != "POST":
        return JsonResponse({"error": "طريقة الطلب يجب أن تكون POST"}, status=405)

    try:
        data = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"error": "صيغة JSON غير صحيحة"}, status=400)

    phone = data.get("phone")
    if not phone:
        return JsonResponse({"error": "يرجى إدخال رقم الجوال"}, status=400)

    otp = generate_otp(phone)

    return JsonResponse({
        "message": "تم إرسال كود التحقق",
        "otp_debug": otp,   # يظهر فقط أثناء التطوير
    }, status=200)


# ==========================================================
# 📌 التحقق من الكود + تسجيل الدخول
# ==========================================================
@csrf_exempt
def verify_and_login(request):
    """التحقق من كود OTP وتسجيل دخول المستخدم"""
    if request.method != "POST":
        return JsonResponse({"error": "طريقة الطلب يجب أن تكون POST"}, status=405)

    try:
        data = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"error": "صيغة JSON غير صحيحة"}, status=400)

    phone = data.get("phone")
    code = data.get("code")

    if not phone or not code:
        return JsonResponse({"error": "رقم الجوال والكود مطلوبان"}, status=400)

    if not verify_otp(phone, code):
        return JsonResponse({"error": "الكود غير صحيح أو منتهي"}, status=400)

    # جلب أو إنشاء مستخدم
    user, created = CustomUser.objects.get_or_create(phone=phone)

    login(request, user)
    request.session["customer_phone"] = user.phone

    return JsonResponse({
        "message": "تم تسجيل الدخول بنجاح",
        "new_user": created,
        "redirect": "/accounts/dashboard/"
    }, status=200)


# ==========================================================
# 📌 صفحة الداشبورد (الأهم)
# ==========================================================
def customer_dashboard(request):
    """لوحة العميل — تعرض الحجز القادم والحجوزات السابقة"""

    if not request.user.is_authenticated:
        return redirect("accounts:login")

    # جميع حجوزات المستخدم
    bookings = Booking.objects.filter(user=request.user).order_by("date", "time__time")

    # تقسيم الحجوزات
    today = date.today()
    upcoming_booking = bookings.filter(date__gte=today).first()
    previous_bookings = bookings.filter(date__lt=today)

    return render(request, "dashboard.html", {
        "phone": request.user.phone,
        "upcoming_booking": upcoming_booking,
        "previous_bookings": previous_bookings,
    })



# ==========================================================
# 📌 صفحة قائمة الخدمات
# ==========================================================
def services_page(request):
    return render(request, "services.html")


# ==========================================================
# 📌 صفحة تواصل معنا
# ==========================================================
def contact_page(request):
    return render(request, "contact.html")
