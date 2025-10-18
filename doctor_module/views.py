from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from patient_module.models import Appointment, MedicalHistory
from .models import Prescription, DoctorSchedule, TreatmentPlan
from .forms import PrescriptionForm, DoctorScheduleForm, TreatmentPlanForm , MedicalHistoryForm

@login_required
def doctor_dashboard(request):
    if request.user.user_type != 'doctor':
        messages.error(request, 'Access denied')
        return redirect('core:home')
    
    today_appointments = Appointment.objects.filter(
        doctor=request.user, 
        status='scheduled'
    ).order_by('appointment_time')[:5]
    
    total_patients = Appointment.objects.filter(doctor=request.user).values('patient').distinct().count()
    total_appointments = Appointment.objects.filter(doctor=request.user).count()
    
    context = {
        'today_appointments': today_appointments,
        'total_patients': total_patients,
        'total_appointments': total_appointments,
    }
    return render(request, 'doctor/dashboard.html', context)

@login_required
def appointment_schedule(request):
    if request.user.user_type != 'doctor':
        return redirect('core:home')
    
    appointments = Appointment.objects.filter(doctor=request.user).order_by('-appointment_date')
    return render(request, 'doctor/appointments.html', {'appointments': appointments})

@login_required
def patient_records(request):
    if request.user.user_type != 'doctor':
        return redirect('core:home')
    
    appointments = Appointment.objects.filter(doctor=request.user).values('patient').distinct()
    patient_ids = [apt['patient'] for apt in appointments]
    from core.models import User
    patients = User.objects.filter(id__in=patient_ids)
    
    return render(request, 'doctor/patient_records.html', {'patients': patients})

@login_required
def patient_detail(request, patient_id):
    if request.user.user_type != 'doctor':
        return redirect('core:home')
    
    from core.models import User
    patient = get_object_or_404(User, id=patient_id)
    medical_history = MedicalHistory.objects.filter(patient=patient)
    appointments = Appointment.objects.filter(patient=patient, doctor=request.user)
    prescriptions = Prescription.objects.filter(patient=patient, doctor=request.user)
    
    context = {
        'patient': patient,
        'medical_history': medical_history,
        'appointments': appointments,
        'prescriptions': prescriptions,
    }
    return render(request, 'doctor/patient_detail.html', context)

@login_required
def create_prescription(request, appointment_id):
    if request.user.user_type != 'doctor':
        return redirect('core:home')
    
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=request.user)
    
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.appointment = appointment
            prescription.patient = appointment.patient
            prescription.doctor = request.user
            prescription.save()
            messages.success(request, 'Prescription created successfully')
            return redirect('doctor:patient_detail', patient_id=appointment.patient.id)
    else:
        form = PrescriptionForm()
    
    return render(request, 'doctor/create_prescription.html', {'form': form, 'appointment': appointment})

@login_required
def prescriptions_list(request):
    if request.user.user_type != 'doctor':
        return redirect('core:home')
    
    prescriptions = Prescription.objects.filter(doctor=request.user).order_by('-created_at')
    return render(request, 'doctor/prescriptions.html', {'prescriptions': prescriptions})

@login_required
def manage_schedule(request):
    if request.user.user_type != 'doctor':
        return redirect('core:home')
    
    schedules = DoctorSchedule.objects.filter(doctor=request.user)
    
    if request.method == 'POST':
        form = DoctorScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.doctor = request.user
            schedule.save()
            messages.success(request, 'Schedule added successfully')
            return redirect('doctor:manage_schedule')
    else:
        form = DoctorScheduleForm()
    
    return render(request, 'doctor/schedule.html', {'schedules': schedules, 'form': form})

@login_required
def create_treatment_plan(request, patient_id):
    if request.user.user_type != 'doctor':
        return redirect('core:home')
    
    from core.models import User
    patient = get_object_or_404(User, id=patient_id)
    
    if request.method == 'POST':
        form = TreatmentPlanForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.patient = patient
            plan.doctor = request.user
            plan.save()
            messages.success(request, 'Treatment plan created successfully')
            return redirect('doctor:patient_detail', patient_id=patient.id)
    else:
        form = TreatmentPlanForm()
    
    return render(request, 'doctor/create_treatment_plan.html', {'form': form, 'patient': patient})



@login_required
def add_medical_history(request, patient_id):
    if request.user.user_type != 'doctor':
        return redirect('core:home')
    
    from core.models import User
    patient = get_object_or_404(User, id=patient_id)
    
    if request.method == 'POST':
        form = MedicalHistoryForm(request.POST)
        if form.is_valid():
            history = form.save(commit=False)
            history.patient = patient
            history.recorded_by = request.user  # The doctor who's logged in
            history.save()
            messages.success(request, 'Medical history added successfully')
            return redirect('doctor:patient_detail', patient_id=patient.id)
    else:
        form = MedicalHistoryForm()
    
    return render(request, 'doctor/add_medical_history.html', {
        'form': form, 
        'patient': patient
    })