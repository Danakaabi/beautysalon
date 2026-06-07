from django.shortcuts import render

def home_view(request):
    return render(request, "home.html")

def profile_view(request):
    return render(request, "profile.html")

def services_view(request):
    return render(request, "services.html")

def select_time_view(request):
    return render(request, "select_time.html")

def booking_summary_view(request):
    return render(request, "booking_summary.html")

def booking_confirm_view(request):
    return render(request, "booking_confirm.html")

def appointments_view(request):
    return render(request, "appointments.html")

def appointment_detail_view(request, pk):
    return render(request, "appointment_detail.html", {"pk": pk})

def contact_view(request):
    return render(request, "contact.html")
