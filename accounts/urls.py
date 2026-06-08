from django.urls import path

from .views import (
    login_page,
    otp_verify_view,
    send_otp,
    verify_and_login,
    customer_dashboard,
    services_page,
    contact_page,
    dev_last_otp,
)

app_name = "accounts"

urlpatterns = [

    # ==================================================
    # Authentication
    # ==================================================

    # صفحة تسجيل الدخول
    path(
        "login/",
        login_page,
        name="login_page"
    ),

    # صفحة إدخال رمز التحقق
    path(
        "otp-verify/",
        otp_verify_view,
        name="otp_verify"
    ),

    # API إرسال OTP
    path(
        "send-otp/",
        send_otp,
        name="send_otp"
    ),

    # API التحقق من OTP وتسجيل الدخول
    path(
        "verify/",
        verify_and_login,
        name="verify_otp"
    ),

    # ==================================================
    # Customer Pages
    # ==================================================

    # لوحة العميل
    path(
        "dashboard/",
        customer_dashboard,
        name="dashboard"
    ),

    # الخدمات
    path(
        "services/",
        services_page,
        name="services"
    ),

    # تواصل معنا
    path(
        "contact/",
        contact_page,
        name="contact"
    ),

    # ==================================================
    # Development Only
    # ==================================================

    path(
        "dev-last-otp/",
        dev_last_otp,
        name="dev_last_otp"
    ),
]