from django.urls import path
from . import views

app_name = "scheduling"

urlpatterns = [
    path(
        "staff/dashboard/",
        views.staff_dashboard,
        name="staff_dashboard",
    ),

    path(
        "staff/bookings/",
        views.staff_bookings,
        name="staff_bookings",
    ),

    path(
        "staff/bookings/<int:booking_id>/",
        views.booking_detail,
        name="booking_detail",
    ),

    path(
        "staff/bookings/<int:booking_id>/start/",
        views.start_booking_service,
        name="start_booking_service",
    ),

    path(
        "staff/bookings/<int:booking_id>/complete/",
        views.complete_booking_service,
        name="complete_booking_service",
    ),

    path(
        "staff/schedule/",
        views.staff_schedule,
        name="staff_schedule",
    ),

    path(
        "staff/profile/",
        views.staff_profile,
        name="staff_profile",
    ),

    path(
        "staff/availability/",
        views.staff_availability,
        name="staff_availability",
    ),

    path(
        "staff/notifications/",
        views.staff_notifications,
        name="staff_notifications",
    ),
]