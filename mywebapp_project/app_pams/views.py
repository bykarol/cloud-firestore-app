from django.shortcuts import render, redirect
from django.contrib import messages
from . forms import PatientForm
from .models import Patient

# Create your views here.
def homepage(request):
    patients = Patient.objects.all()
    return render(request, "homepage.html", {'patients': patients})

def newpatient(request):
  if request.method == 'POST':
     form = PatientForm(request.POST)
     if form.is_valid():
        form.save()
        messages.success(request, 'Patient added successfully!')
        return redirect("/newpatient")
     else:
            # Loop through form.errors to identify specific errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error in {field}: {error}')
  else:
     form = PatientForm()
  return render(request, "patientform.html", {'form': form})
