from django.urls import path
from . import views

app_name = 'doctor'

urlpatterns = [
    path('dashboard/', views.doctor_dashboard, name='dashboard'),
    path('appointments/', views.appointment_schedule, name='appointments'),
    path('patients/', views.patient_records, name='patient_records'),
    path('patients/<int:patient_id>/', views.patient_detail, name='patient_detail'),
    path('prescriptions/', views.prescriptions_list, name='prescriptions'),
    path('prescriptions/create/<int:appointment_id>/', views.create_prescription, name='create_prescription'),
    path('schedule/', views.manage_schedule, name='manage_schedule'),
    path('treatment-plan/create/<int:patient_id>/', views.create_treatment_plan, name='create_treatment_plan'),
]