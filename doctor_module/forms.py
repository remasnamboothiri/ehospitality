from django import forms
from .models import Prescription, DoctorSchedule, TreatmentPlan

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['medication_name', 'dosage', 'frequency', 'duration', 
                  'instructions', 'drug_interactions_checked']
        widgets = {
            'instructions': forms.Textarea(attrs={'rows': 4}),
        }

class DoctorScheduleForm(forms.ModelForm):
    class Meta:
        model = DoctorSchedule
        fields = ['day_of_week', 'start_time', 'end_time', 'is_available']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

class TreatmentPlanForm(forms.ModelForm):
    class Meta:
        model = TreatmentPlan
        fields = ['diagnosis', 'treatment_description', 'start_date', 'end_date', 'goals']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'treatment_description': forms.Textarea(attrs={'rows': 4}),
            'goals': forms.Textarea(attrs={'rows': 3}),
        }