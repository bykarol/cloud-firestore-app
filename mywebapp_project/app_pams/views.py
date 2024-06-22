import os
from django.shortcuts import render, redirect
from django.contrib import messages
from . forms import PatientForm
from django.conf import settings
from firebase_admin import firestore
import datetime

# Use a service account.
service_account_path = os.path.join(settings.BASE_DIR, 'config', 'serviceAccount.json')
# Verifying if the file exists
if not os.path.exists(service_account_path):
    raise FileNotFoundError(f"serviceAccount.json file not found in the route: {service_account_path}")

# Database connection
db = firestore.client()

# Display list of patients in Homepage
def homepage(request):
   patients_ref = db.collection("patients")
   patients = patients_ref.stream()
   patients_list = []
   for patient in patients:
       patient_dict = patient.to_dict()
       # Adding the id to the each patient
       patient_dict['id'] = patient.id
      # Format date_of_birth to YYYY-MM-DD
       if 'date_of_birth' in patient_dict and isinstance(patient_dict['date_of_birth'], datetime.date):
           patient_dict['date_of_birth'] = patient_dict['date_of_birth'].strftime('%d-%m-%Y')
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

# Update a patient
def updatepatient(request, patient_id):
    try:
        # Getting the patient
        patient_ref = db.collection('patients').document(patient_id)
        patient = patient_ref.get()

        # Verifying if patient exists in Firestore
        if patient.exists:
            # Extract the data from the document
            patient_data = patient.to_dict()

            # parsing date
            if 'date_of_birth' in patient_data:
                patient_data['date_of_birth'] = patient_data['date_of_birth'].strftime('%Y-%m-%d')

            # Setting the form with the current patient data
            form = PatientForm(initial=patient_data)

            # Sent form updated
            if request.method == 'POST':
                form = PatientForm(request.POST)

                if form.is_valid():
                    # Updating the patient with the new data
                    newpatientdata = form.cleaned_data
                    if 'date_of_birth' in newpatientdata and isinstance(newpatientdata['date_of_birth'], datetime.date):
                        newpatientdata['date_of_birth'] = datetime.datetime.combine(newpatientdata['date_of_birth'], datetime.datetime.min.time())
                    patient_ref.update(newpatientdata)
                    messages.success(request, f'Patient with ID {patient_id} updated successfully!')
                    return redirect('homepage')

            # Render form with user data
            context = {
                'patient': patient_data,
            }
            return render(request, 'updatepatient.html', context)
        else:
            # Patient doesn't exist
            messages.error(request, f'Patient with ID {patient_id} does not exist.')
            return redirect('homepage')

    except Exception as e:
        # Any exception redirect to homepage
        messages.error(request, f'Error updating patient details: {e}')
        return redirect('homepage')

# Delete a patient
def deletepatient(request, patient_id):
    try:
        # Deleting the document by id
        db.collection('patients').document(patient_id).delete()
        messages.success(request, f'Patient with ID {patient_id} deleted successfully!')
    except Exception as e:
        messages.error(request, f'Error deleting patient: {e}')

    return redirect('homepage')
