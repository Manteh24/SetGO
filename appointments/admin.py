from django.contrib import admin
from .models import AppointmentRequest

@admin.register(AppointmentRequest)
class AppointmentRequestAdmin(admin.ModelAdmin):
    list_display = ['trainee', 'trainer', 'date', 'start_time', 'end_time', 'status']
    list_filter = ['status', 'date', 'trainer']
