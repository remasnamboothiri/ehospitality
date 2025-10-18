from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Appointment, MedicalHistory, Billing, HealthEducation

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'appointment_date', 'appointment_time', 'status']
    list_filter = ['status', 'appointment_date']
    search_fields = ['patient__username', 'doctor__username']

@admin.register(MedicalHistory)
class MedicalHistoryAdmin(admin.ModelAdmin):
    list_display = ['patient', 'diagnosis', 'date_recorded']
    search_fields = ['patient__username', 'diagnosis']

@admin.register(Billing)
class BillingAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'patient', 'amount', 'payment_status']
    list_filter = ['payment_status']

@admin.register(HealthEducation)
class HealthEducationAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'created_at']