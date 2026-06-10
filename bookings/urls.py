from django.urls import path
from . import views

app_name = "bookings"

urlpatterns = [
    # اختيار الخدمة
    path(
        "services/",
        views.select_service_view,
        name="select_service",
    ),

    # اختيار التاريخ والوقت
    path(
        "date-time/",
        views.select_date_time_view,
        name="select_date_time",
    ),

    # صفحة التأكيد قبل الحجز
    path(
        "confirm/",
        views.confirm_booking_view,
        name="confirm_booking",
    ),

    # تنفيذ الحجز النهائي
    path(
        "complete/",
        views.complete_booking_view,
        name="complete_booking",
    ),

    # صفحة نجاح الحجز
    path(
        "success/",
        views.booking_success_view,
        name="booking_success",
    ),

    # حجوزات العميل
    path(
        "my-bookings/",
        views.my_bookings_view,
        name="my_bookings",
    ),

    # إلغاء / تعديل حجز العميل
    path(
        "cancel/<int:booking_id>/",
        views.cancel_booking,
        name="cancel_booking",
    ),
    path(
        "edit/<int:booking_id>/",
        views.edit_booking,
        name="edit_booking",
    ),

    # إجراءات الموظفة على الحجز
    path(
        "staff/bookings/<int:booking_id>/start/",
        views.start_service,
        name="start_service",
    ),
    path(
        "staff/bookings/<int:booking_id>/complete/",
        views.complete_service,
        name="complete_service",
    ),
    path(
    "staff/bookings/<int:booking_id>/",
    views.booking_detail,
    name="booking_detail",
),
]