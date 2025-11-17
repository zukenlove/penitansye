from .models  import Appointment
from django  import forms

from django import forms
from .models import Appointment, Patient

from django import forms
from .models import Patient

class PatientForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Patient
        fields = ['firstname', 'lastname', 'date_of_birth', 'phone', 'email', 'password', 'symptoms']

    def save(self, commit=True):
        patient = super().save(commit=False)
        # Hash the password before saving
        patient.set_password(self.cleaned_data['password'])
        if commit:
            patient.save()
        return patient


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = [
            "patient",
            "doctor",
            "clinic",
            "visit_date",
            "treatment",
        ]
        widgets = {
            "visit_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }
