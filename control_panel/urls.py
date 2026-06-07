from django.urls import path
from . import views

app_name = "control_panel"

urlpatterns = [

    # الصفحة الرئيسية للوحة التحكم
    path("", views.dashboard_home, name="dashboard_home"),

    # إدارة الموظفين (لاحقاً إذا احتجتيها)
    path("staff/", views.staff_list, name="staff_list"),

    # صفحة الإعدادات العامة للصالون
    path("settings/", views.settings_page, name="settings_page"),

    # عرض الحجوزات (نضيفها لاحقاً)
    path("bookings/", views.bookings_list, name="bookings_list"),
   path("staff/base-preview/", views.preview_staff_base, name="preview_staff_base"),


]
