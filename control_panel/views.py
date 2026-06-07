from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# ==========================================================
# 🏠 الصفحة الرئيسية للوحة التحكم (المديرة)
# ==========================================================
@login_required
def dashboard_home(request):
    return render(request, "control_panel/dashboard_home.html")


# ==========================================================
# 👩‍💼 قائمة الموظفين (لاحقًا نضيف موديل Staff)
# ==========================================================
@login_required
def staff_list(request):
    return render(request, "control_panel/staff_list.html")


# ==========================================================
# ⚙️ إعدادات الصالون
# ==========================================================
@login_required
def settings_page(request):
    return render(request, "control_panel/settings_page.html")


# ==========================================================
# 📅 عرض الحجوزات في لوحة التحكم
# ==========================================================
@login_required
def bookings_list(request):
    return render(request, "control_panel/bookings_list.html")


# ==========================================================
# 🌟 استعراض صفحة الـ BASE الخاصة بالموظفة (Preview Only)
# ==========================================================
@login_required
def preview_staff_base(request):
    return render(request, "staff/preview_base.html")
