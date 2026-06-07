# salon_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # حساب المستخدم
    path('accounts/', include('accounts.urls')),

    # الخدمات
    path('catalog/', include('catalog.urls')),

    # اوقات العمل
    path('schedule/', include('scheduling.urls')),

    # الحجوزات
    path('bookings/', include('bookings.urls')),

    # الدفع
    path('billing/', include('billing.urls')),

    # الإشعارات
    path('notifications/', include('notifications_center.urls')),

    # بوابة العميل (الصفحة الرئيسية)
    path('', include('portal_client.urls')),

    # لوحة الإدارة
    path('dashboard/', include('control_panel.urls')),

    # لوحة المشرف Django
    path('admin/', admin.site.urls),
]


# Static & Media
if settings.DEBUG:

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    if hasattr(settings, "STATICFILES_DIRS") and settings.STATICFILES_DIRS:
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    else:
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
