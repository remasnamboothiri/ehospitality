from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm

def home(request):
    context = {
        'is_home_page': True  # This tells the template it's the home page
    }
    return render(request, 'home.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            
            if user.user_type == 'patient':
                return redirect('patient:dashboard')
            elif user.user_type == 'doctor':
                return redirect('doctor:dashboard')
            elif user.user_type == 'admin':
                return redirect('hospital_admin:dashboard')  # ← FIXED
            return redirect('core:home')
    else:
        form = UserRegistrationForm()
    return render(request, 'core/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                
                if user.user_type == 'patient':
                    messages.success(request, f'Welcome {user.username}!')
                    return redirect('patient:dashboard')
                elif user.user_type == 'doctor':
                    messages.success(request, f'Welcome Dr. {user.username}!')
                    return redirect('doctor:dashboard')
                elif user.user_type == 'admin':
                    messages.success(request, f'Welcome Admin {user.username}!')
                    return redirect('hospital_admin:dashboard')  # ← FIXED
                return redirect('core:home')
            else:
                messages.error(request, 'Invalid credentials')
    else:
        form = UserLoginForm()
    return render(request, 'core/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('core:home')