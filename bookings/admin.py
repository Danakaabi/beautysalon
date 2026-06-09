from django.contrib import admin
from .models import TimeSlot, Booking, BookingItem


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ("id", "time")
    ordering = ("time",)


class BookingItemInline(admin.TabularInline):
    model = BookingItem
    extra = 0


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "date", "time", "staff_member", "status", "total_amount")
    list_filter = ("status", "date", "staff_member")
    search_fields = ("user__phone", "staff_member__name")
    inlines = [BookingItemInline]


@admin.register(BookingItem)
class BookingItemAdmin(admin.ModelAdmin):
    list_display = ("id", "booking", "service", "price_at_booking", "duration_at_booking")