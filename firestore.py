import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account.
cred = credentials.Certificate('./serviceAccount.json')

app = firebase_admin.initialize_app(cred)

db = firestore.client()

# Adding data
doc_ref = db.collection("patients").document()
doc_ref.set({"firstname": "Test", "lastname": "Testing", "email":"test@gmail.com", "date_of_birth": 1815})


# Reading data
patients_ref = db.collection("patients")
docs = patients_ref.stream()

for doc in docs:
    print(f"{doc.id} => {doc.to_dict()}")