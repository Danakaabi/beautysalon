from django.contrib import admin
from .models import Staff, StaffService


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "phone")


@admin.register(StaffService)
class StaffServiceAdmin(admin.ModelAdmin):
    list_display = ("id", "staff", "service")