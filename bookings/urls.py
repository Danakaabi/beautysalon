# bookings/urls.py
from django.urls import path
from . import views

app_name = "bookings"

urlpatterns = [

    # ============================================================
    # 1) اختيار الخدمة
    # ============================================================
    path("services/", views.select_service_view, name="select_service"),

    # ============================================================
    # 2) اختيار التاريخ والوقت (بدون اختيار موظفة)
    # ============================================================
    path("date-time/", views.select_date_time_view, name="select_date_time"),

    # ============================================================
    # 3) صفحة التأكيد قبل الحجز
    # ============================================================
    path("confirm/", views.confirm_booking_view, name="confirm_booking"),

    # ============================================================
    # 4) تنفيذ الحجز النهائي
    # ============================================================
    path("complete/", views.complete_booking_view, name="complete_booking"),

    # ============================================================
    # 5) صفحة نجاح الحجز
    # ============================================================
    path("success/", views.booking_success_view, name="booking_success"),

    # ============================================================
    # 6) حجوزات العميل (لاحقاً تربط بقاعدة البيانات)
    # ============================================================
    path("my-bookings/", views.my_bookings_view, name="my_bookings"),
    path("cancel/<int:booking_id>/", views.cancel_booking, name="cancel_booking"),
    path("edit/<int:booking_id>/", views.edit_booking, name="edit_booking"),

]
