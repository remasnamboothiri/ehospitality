from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.models import User
from patient_module.models import Appointment
from .models import Facility, Department
from .forms import UserManagementForm, FacilityForm, DepartmentForm
from patient_module.models import Billing
from .forms import BillingForm  # Add this to your imports at the top

@login_required
def admin_dashboard(request):
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied. Administrator privileges required.')
        return redirect('core:home')
    
    total_users = User.objects.count()
    total_patients = User.objects.filter(user_type='patient').count()
    total_doctors = User.objects.filter(user_type='doctor').count()
    total_appointments = Appointment.objects.count()
    pending_appointments = Appointment.objects.filter(status='scheduled').count()
    total_facilities = Facility.objects.count()
    total_departments = Department.objects.count()
    
    recent_appointments = Appointment.objects.all().order_by('-created_at')[:5]
    recent_users = User.objects.all().order_by('-date_joined')[:5]
    
    context = {
        'total_users': total_users,
        'total_patients': total_patients,
        'total_doctors': total_doctors,
        'total_appointments': total_appointments,
        'pending_appointments': pending_appointments,
        'total_facilities': total_facilities,
        'total_departments': total_departments,
        'recent_appointments': recent_appointments,
        'recent_users': recent_users,
    }
    return render(request, 'admin/dashboard.html', context)

@login_required
def user_management(request):
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied. Administrator privileges required.')
        return redirect('core:home')
    
    users = User.objects.all().order_by('-date_joined')
    
    # Filter by user type if requested
    user_type_filter = request.GET.get('type')
    if user_type_filter:
        users = users.filter(user_type=user_type_filter)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        users = users.filter(
            username__icontains=search_query
        ) | users.filter(
            email__icontains=search_query
        ) | users.filter(
            first_name__icontains=search_query
        ) | users.filter(
            last_name__icontains=search_query
        )
    
    context = {
        'users': users,
        'user_type_filter': user_type_filter,
        'search_query': search_query,
    }
    return render(request, 'admin/user_management.html', context)

@login_required
def add_user(request):
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied. Administrator privileges required.')
        return redirect('core:home')
    
    if request.method == 'POST':
        form = UserManagementForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            if password:
                user.set_password(password)
            else:
                # Set default password if none provided
                user.set_password('Welcome@123')
            user.save()
            messages.success(request, f'User {user.username} created successfully!')
            return redirect('admin:user_management')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserManagementForm()
    
    return render(request, 'admin/add_user.html', {'form': form})

@login_required
def edit_user(request, user_id):
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied. Administrator privileges required.')
        return redirect('core:home')
    
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = UserManagementForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            updated_user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            if password:
                updated_user.set_password(password)
            updated_user.save()
            messages.success(request, f'User {updated_user.username} updated successfully!')
            return redirect('admin:user_management')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserManagementForm(instance=user)
    
    context = {
        'form': form,
        'user': user,
        'editing': True,
    }
    return render(request, 'admin/edit_user.html', context)

@login_required
def delete_user(request, user_id):
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied. Administrator privileges required.')
        return redirect('core:home')
    
    user = get_object_or_404(User, id=user_id)
    
    # Prevent deleting yourself
    if user == request.user:
        messages.error(request, 'You cannot delete your own account!')
        return redirect('admin:user_management')
    
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f'User {username} deleted successfully!')
        return redirect('admin:user_management')
    
    return render(request, 'admin/delete_user.html', {'user': user})

@login_required
def toggle_user_status(request, user_id):
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('core:home')
    
    user = get_object_or_404(User, id=user_id)
    user.is_active = not user.is_active
    user.save()
    
    status = "activated" if user.is_active else "deactivated"
    messages.success(request, f'User {user.username} has been {status}.')
    return redirect('admin:user_management')

@login_required
def facility_management(request):
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied. Administrator privileges required.')
        return redirect('core:home')
    
    facilities = Facility.objects.all().order_by('name')
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        facilities = facilities.filter(
            name__icontains=search_query
        ) | facilities.filter(
            location__icontains=search_query
        )
    
    context = {
        'facilities': facilities,
        'search_query': search_query,
    }
    return render(request, 'admin/facility_management.html', context)

@login_required
def add_facility(request):
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied. Administrator privileges required.')
        return redirect('core:home')
    
    if request.method == 'POST':
        form = FacilityForm(request.POST)
        if form.is_valid():
            facility = form.save()
            messages.success(request, f'Facility "{facility.name}" created successfully!')
            return redirect('hospital_admin:facility_management')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = FacilityForm()
    
    return render(request, 'admin/add_facility.html', {'form': form})

@login_required
def edit_facility(request, facility_id):
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied. Administrator privileges required.')
        return redirect('core:home')
    
    facility = get_object_or_404(Facility, id=facility_id)
    
    if request.method == 'POST':
        form = FacilityForm(request.POST, instance=facility)
        if form.is_valid():
            updated_facility = form.save()
            messages.success(request, f'Facility "{updated_facility.name}" updated successfully!')
            return redirect('hospital_admin:facility_management')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = FacilityForm(instance=facility)
    
    context = {
        'form': form,
        'facility': facility,
        'editing': True,
    }
    return render(request, 'admin/edit_facility.html', context)

@login_required
def delete_facility(request, facility_id):
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied. Administrator privileges required.')
        return redirect('core:home')
    
    facility = get_object_or_404(Facility, id=facility_id)
    
    if request.method == 'POST':
        facility_name = facility.name
        facility.delete()
        messages.success(request, f'Facility "{facility_name}" deleted successfully!')
        return redirect('hospital_admin:facility_management')
    
    return render(request, 'admin/delete_facility.html', {'facility': facility})

@login_required
def appointment_management(request):
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied. Administrator privileges required.')
        return redirect('core:home')
    
    appointments = Appointment.objects.all().select_related(
        'patient', 'doctor'
    ).order_by('-appointment_date', '-appointment_time')
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        appointments = appointments.filter(status=status_filter)
    
    # Filter by date
    date_filter = request.GET.get('date')
    if date_filter:
        appointments = appointments.filter(appointment_date=date_filter)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        appointments = appointments.filter(
            patient__username__icontains=search_query
        ) | appointments.filter(
            doctor__username__icontains=search_query
        ) | appointments.filter(
            patient__first_name__icontains=search_query
        ) | appointments.filter(
            patient__last_name__icontains=search_query
        )
    
    context = {
        'appointments': appointments,
        'status_filter': status_filter,
        'date_filter': date_filter,
        'search_query': search_query,
    }
    return render(request, 'admin/appointment_management.html', context)

@login_required
def appointment_detail(request, appointment_id):
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied. Administrator privileges required.')
        return redirect('core:home')
    
    appointment = get_object_or_404(
        Appointment.objects.select_related('patient', 'doctor'),
        id=appointment_id
    )
    
    return render(request, 'admin/appointment_detail.html', {'appointment': appointment})

@login_required
def update_appointment_status(request, appointment_id):
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('core:home')
    
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Appointment.STATUS_CHOICES):
            appointment.status = new_status
            appointment.save()
            messages.success(request, f'Appointment status updated to {appointment.get_status_display()}')
        else:
            messages.error(request, 'Invalid status')
    
    return redirect('hospital_admin:appointment_management')

@login_required
def department_management(request):
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied. Administrator privileges required.')
        return redirect('core:home')
    
    departments = Department.objects.all().select_related('facility').order_by('facility', 'name')
    
    # Filter by facility
    facility_filter = request.GET.get('facility')
    if facility_filter:
        departments = departments.filter(facility_id=facility_filter)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        departments = departments.filter(
            name__icontains=search_query
        ) | departments.filter(
            head_of_department__icontains=search_query
        )
    
    facilities = Facility.objects.all()
    
    context = {
        'departments': departments,
        'facilities': facilities,
        'facility_filter': facility_filter,
        'search_query': search_query,
    }
    return render(request, 'admin/department_management.html', context)

@login_required
def add_department(request):
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied. Administrator privileges required.')
        return redirect('core:home')
    
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            department = form.save()
            messages.success(request, f'Department "{department.name}" created successfully!')
            return redirect('hospital_admin:department_management')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = DepartmentForm()
    
    return render(request, 'admin/add_department.html', {'form': form})

@login_required
def edit_department(request, department_id):
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied. Administrator privileges required.')
        return redirect('core:home')
    
    department = get_object_or_404(Department, id=department_id)
    
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            updated_department = form.save()
            messages.success(request, f'Department "{updated_department.name}" updated successfully!')
            return redirect('hospital_admin:department_management')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = DepartmentForm(instance=department)
    
    context = {
        'form': form,
        'department': department,
        'editing': True,
    }
    return render(request, 'admin/edit_department.html', context)

@login_required
def delete_department(request, department_id):
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied. Administrator privileges required.')
        return redirect('core:home')
    
    department = get_object_or_404(Department, id=department_id)
    
    if request.method == 'POST':
        department_name = department.name
        department.delete()
        messages.success(request, f'Department "{department_name}" deleted successfully!')
        return redirect('hospital_admin:department_management')
    
    return render(request, 'admin/delete_department.html', {'department': department})

@login_required
def system_reports(request):
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied. Administrator privileges required.')
        return redirect('core:home')
    
    from django.db.models import Count, Q
    from datetime import datetime, timedelta
    
    # Get statistics
    today = datetime.now().date()
    last_month = today - timedelta(days=30)
    
    # User statistics
    new_users_this_month = User.objects.filter(date_joined__gte=last_month).count()
    active_users = User.objects.filter(is_active=True).count()
    
    # Appointment statistics
    appointments_this_month = Appointment.objects.filter(created_at__gte=last_month).count()
    completed_appointments = Appointment.objects.filter(status='completed').count()
    cancelled_appointments = Appointment.objects.filter(status='cancelled').count()
    
    # User type breakdown
    user_type_stats = User.objects.values('user_type').annotate(count=Count('id'))
    
    context = {
        'new_users_this_month': new_users_this_month,
        'active_users': active_users,
        'appointments_this_month': appointments_this_month,
        'completed_appointments': completed_appointments,
        'cancelled_appointments': cancelled_appointments,
        'user_type_stats': user_type_stats,
        'today': today,
    }
    
    return render(request, 'admin/system_reports.html', context)






# Billing views would go here if you have them
@login_required
def billing_management(request):
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('core:home')
    
    from patient_module.models import Billing
    billings = Billing.objects.all().select_related('patient').order_by('-created_at')
    
    context = {
        'billings': billings,
    }
    return render(request, 'admin/billing_management.html', context)

@login_required
def add_billing(request):
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('core:home')
    
    from admin_module.forms import BillingForm
    if request.method == 'POST':
        form = BillingForm(request.POST)
        if form.is_valid():
            billing = form.save()
            messages.success(request, f'Billing record {billing.invoice_number} created successfully!')
            return redirect('hospital_admin:billing_management')  # ← FIXED!
    else:
        form = BillingForm()
    
    return render(request, 'admin/add_billing.html', {'form': form})

@login_required
def edit_billing(request, billing_id):
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('core:home')
    
    from patient_module.models import Billing
    from admin_module.forms import BillingForm
    
    billing = get_object_or_404(Billing, id=billing_id)
    
    if request.method == 'POST':
        form = BillingForm(request.POST, instance=billing)
        if form.is_valid():
            updated_billing = form.save()
            messages.success(request, f'Billing {updated_billing.invoice_number} updated successfully!')
            return redirect('hospital_admin:billing_management')  # ← FIXED!
    else:
        form = BillingForm(instance=billing)
    
    context = {
        'form': form,
        'billing': billing,
        'editing': True,
    }
    return render(request, 'admin/edit_billing.html', context)

@login_required
def delete_billing(request, billing_id):
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('core:home')
    
    from patient_module.models import Billing
    billing = get_object_or_404(Billing, id=billing_id)
    
    if request.method == 'POST':
        invoice_number = billing.invoice_number
        billing.delete()
        messages.success(request, f'Billing {invoice_number} deleted successfully!')
        return redirect('hospital_admin:billing_management')  # ← FIXED!
    
    return render(request, 'admin/delete_billing.html', {'billing': billing})