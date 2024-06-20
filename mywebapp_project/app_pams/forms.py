from django import forms
from . models import Patient

class PatientForm(forms.ModelForm):
  class Meta:
    model = Patient
    fields = [
      'firstname',
      'lastname',
      'email',
      'date_of_birth'  
    ]
