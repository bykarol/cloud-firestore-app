from django import forms
from . models import Patient

class PatientForm(forms.ModelForm):
  class Meta:
    model = Patient
    fields = [
      'patient_firstname',
      'patient_lastname',
      'email',
      'date_of_birth'  
    ]
