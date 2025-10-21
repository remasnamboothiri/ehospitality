from django import forms
from core.models import User
from .models import Facility, Department
from patient_module.models import Billing, Appointment
import random
import string

class UserManagementForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'user_type', 
                  'phone', 'date_of_birth', 'address', 'is_active']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }
    
    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user

class FacilityForm(forms.ModelForm):
    class Meta:
        model = Facility
        fields = ['name', 'location', 'address', 'phone', 'email', 'capacity']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['facility', 'name', 'description', 'head_of_department']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
        
        
        


class BillingForm(forms.ModelForm):
    patient = forms.ModelChoiceField(
        queryset=User.objects.filter(user_type='patient'),
        empty_label="Select Patient"
    )
    appointment = forms.ModelChoiceField(
        queryset=Appointment.objects.all(),
        required=False,
        empty_label="Select Appointment (Optional)"
    )
    
    class Meta:
        model = Billing
        fields = ['patient', 'appointment', 'amount', 'payment_status', 'insurance_info']
        widgets = {
            'amount': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'insurance_info': forms.Textarea(attrs={'rows': 3}),
        }
    
    def save(self, commit=True):
        billing = super().save(commit=False)
        if not billing.invoice_number:
            # Auto-generate invoice number
            random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            billing.invoice_number = f'INV-{random_str}'
        if commit:
            billing.save()
        return billing        