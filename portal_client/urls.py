from django.urls import path
from . import views

app_name = "portal_client"

urlpatterns = [

    # ============================
    # واجهة العميل الأساسية
    # ============================

    # الصفحة الرئيسية (Dashboard / Home)
    path('', views.home_view, name='home'),

    # صفحة الملف الشخصي
    path('profile/', views.profile_view, name='profile'),

    # ============================
    # الخدمات (Services)
    # ============================
    path('services/', views.services_view, name='services'),

    # ============================
    # الحجز (Booking Flow)
    # ============================

    # اختيار الوقت
    path('select-time/', views.select_time_view, name='select_time'),

    # ملخص الحجز قبل التأكيد
    path('booking/summary/', views.booking_summary_view, name='booking_summary'),

    # تأكيد الحجز النهائي
    path('booking/confirm/', views.booking_confirm_view, name='booking_confirm'),

    # ============================
    # المواعيد (Appointments)
    # ============================

    # مواعيدي
    path('appointments/', views.appointments_view, name='appointments'),

    # تفاصيل موعد واحد
    path('appointments/<int:pk>/', views.appointment_detail_view, name='appointment_detail'),

    # ============================
    # التواصل (Contact)
    # ============================
    path('contact/', views.contact_view, name='contact'),
]
