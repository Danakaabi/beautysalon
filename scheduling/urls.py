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
        "staff/notifications/",
        views.staff_notifications,
        name="staff_notifications",
    ),
]