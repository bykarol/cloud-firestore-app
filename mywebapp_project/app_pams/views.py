import os
from django.shortcuts import render, redirect
from django.contrib import messages
from . forms import PatientForm
from django.conf import settings
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime

# Use a service account.
service_account_path = os.path.join(settings.BASE_DIR, 'config', 'serviceAccount.json')
# Verifying if the file exists
if not os.path.exists(service_account_path):
    raise FileNotFoundError(f"No se encontró el archivo serviceAccount.json en la ruta: {service_account_path}")

cred = credentials.Certificate(service_account_path)
app = firebase_admin.initialize_app(cred)
db = firestore.client()

# Display list of patients in Homepage
def homepage(request):
   #  patients = Patient.objects.all()
   patients_ref = db.collection("patients")
   patients = patients_ref.stream()
   patients_list = []
   for patient in patients:
       patient_dict = patient.to_dict()
       # Adding the id to the each patient
       patient_dict['id'] = patient.id
       patients_list.append(patient_dict)

   return render(request, "homepage.html", {'patients': patients_list})

# Adding a patient
def newpatient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            # Extract data from the form
            patientdata = form.cleaned_data
            # Convert date_of_birth field to datetime object
            if 'date_of_birth' in patientdata and isinstance(patientdata['date_of_birth'], datetime.date):
                patientdata['date_of_birth'] = datetime.datetime.combine(patientdata['date_of_birth'], datetime.datetime.min.time())
            try:
                # Add the patient to Firestore
                db.collection('patients').add(patientdata)
                messages.success(request, 'Patient added successfully!')
                return redirect("/newpatient")
            except Exception as e:
                messages.error(request, f'Error adding patient: {e}')
        else:
            # Loop through form.errors to identify specific errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error in {field}: {error}')
    else:
        form = PatientForm()
    return render(request, "patientform.html", {'form': form})

def updatepatient(request, patient_id):
    return render(request, "updatepatient.html")

# Delete a patient
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Patient

def deletepatient(request, patient_id):
    try:
        # Eliminar el documento usando el ID proporcionado por Firestore
        db.collection('patients').document(patient_id).delete()
        messages.success(request, f'Patient with ID {patient_id} deleted successfully!')
    except Exception as e:
        messages.error(request, f'Error deleting patient: {e}')

    return redirect('homepage')

# TODO: delete cache: email because I have an error adding data that was previous deleted