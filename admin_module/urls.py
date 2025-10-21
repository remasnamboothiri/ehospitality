from django.urls import path
from . import views

app_name = 'hospital_admin' 

urlpatterns = [
    # Dashboard
    path('dashboard/', views.admin_dashboard, name='dashboard'),
    
    # User Management
    path('users/', views.user_management, name='user_management'),
    path('users/add/', views.add_user, name='add_user'),
    path('users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('users/toggle-status/<int:user_id>/', views.toggle_user_status, name='toggle_user_status'),
    
    # Facility Management
    path('facilities/', views.facility_management, name='facility_management'),
    path('facilities/add/', views.add_facility, name='add_facility'),
    path('facilities/edit/<int:facility_id>/', views.edit_facility, name='edit_facility'),
    path('facilities/delete/<int:facility_id>/', views.delete_facility, name='delete_facility'),
    
    # Appointment Management
    path('appointments/', views.appointment_management, name='appointment_management'),
    path('appointments/<int:appointment_id>/', views.appointment_detail, name='appointment_detail'),
    path('appointments/<int:appointment_id>/update-status/', views.update_appointment_status, name='update_appointment_status'),
    
    # Department Management
    path('departments/', views.department_management, name='department_management'),
    path('departments/add/', views.add_department, name='add_department'),
    path('departments/edit/<int:department_id>/', views.edit_department, name='edit_department'),
    path('departments/delete/<int:department_id>/', views.delete_department, name='delete_department'),
    
    # Reports
    path('reports/', views.system_reports, name='system_reports'), 
    
    # Billing Management (ADD THESE LINES)
    path('billing/', views.billing_management, name='billing_management'),
    path('billing/add/', views.add_billing, name='add_billing'),
    path('billing/edit/<int:billing_id>/', views.edit_billing, name='edit_billing'),
    path('billing/delete/<int:billing_id>/', views.delete_billing, name='delete_billing'),
]