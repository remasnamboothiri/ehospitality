from django.urls import path
from . import views

app_name = 'patient'

urlpatterns = [
    path('dashboard/', views.patient_dashboard, name='dashboard'),
    path('book-appointment/', views.book_appointment, name='book_appointment'),
    path('appointments/', views.appointments_list, name='appointments'),
    path('cancel-appointment/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('medical-history/', views.medical_history, name='medical_history'),
    path('billing/', views.billing_list, name='billing'),
    path('health-education/', views.health_education, name='health_education'),
    path('profile/', views.patient_profile, name='profile'),
]