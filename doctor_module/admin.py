from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Prescription, DoctorSchedule, TreatmentPlan

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['medication_name', 'patient', 'doctor', 'created_at']
    search_fields = ['medication_name', 'patient__username']

@admin.register(DoctorSchedule)
class DoctorScheduleAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'day_of_week', 'start_time', 'end_time', 'is_available']
    list_filter = ['day_of_week', 'is_available']

@admin.register(TreatmentPlan)
class TreatmentPlanAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'diagnosis', 'start_date']
    search_fields = ['patient__username', 'diagnosis']