from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.models import User
from .models import Appointment, MedicalHistory, Billing, HealthEducation
from .forms import AppointmentForm, PatientProfileForm

@login_required
def patient_dashboard(request):
    if request.user.user_type != 'patient':
        messages.error(request, 'Access denied')
        return redirect('core:home')
    
    appointments = Appointment.objects.filter(patient=request.user).order_by('-appointment_date')[:5]
    billings = Billing.objects.filter(patient=request.user).order_by('-created_at')[:5]
    context = {
        'appointments': appointments,
        'billings': billings,
    }
    return render(request, 'patient/dashboard.html', context)

@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.save()
            messages.success(request, 'Appointment booked successfully!')
            return redirect('patient:appointments')
    else:
        form = AppointmentForm()
    return render(request, 'patient/book_appointment.html', {'form': form})

@login_required
def appointments_list(request):
    appointments = Appointment.objects.filter(patient=request.user).order_by('-appointment_date')
    return render(request, 'patient/appointments.html', {'appointments': appointments})

@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user)
    appointment.status = 'cancelled'
    appointment.save()
    messages.success(request, 'Appointment cancelled successfully')
    return redirect('patient:appointments')

@login_required
def medical_history(request):
    histories = MedicalHistory.objects.filter(patient=request.user).order_by('-date_recorded')
    return render(request, 'patient/medical_history.html', {'histories': histories})

@login_required
def billing_list(request):
    billings = Billing.objects.filter(patient=request.user).order_by('-created_at')
    return render(request, 'patient/billing.html', {'billings': billings})

@login_required
def health_education(request):
    articles = HealthEducation.objects.all().order_by('-created_at')
    return render(request, 'patient/health_education.html', {'articles': articles})

@login_required
def patient_profile(request):
    if request.method == 'POST':
        form = PatientProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('patient:dashboard')
    else:
        form = PatientProfileForm(instance=request.user)
    return render(request, 'patient/profile.html', {'form': form})