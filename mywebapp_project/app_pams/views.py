import os
from django.shortcuts import render, redirect
from django.contrib import messages
from . forms import PatientForm
from .models import Patient

from django.conf import settings
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account.
service_account_path = os.path.join(settings.BASE_DIR, 'config', 'serviceAccount.json')
# Verifying if the file exists
if not os.path.exists(service_account_path):
    raise FileNotFoundError(f"No se encontró el archivo serviceAccount.json en la ruta: {service_account_path}")

cred = credentials.Certificate(service_account_path)
app = firebase_admin.initialize_app(cred)

db = firestore.client()
# Create your views here.
def homepage(request):
   #  patients = Patient.objects.all()
   patients_ref = db.collection("patients")
   patients = patients_ref.stream()
   patients_list = []
   for patient in patients:
       patients_list.append(patient.to_dict())

   return render(request, "homepage.html", {'patients': patients_list})

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
