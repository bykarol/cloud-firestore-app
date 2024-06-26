﻿# Overview

Building upon my previous project [Django PMS web app](https://github.com/bykarol/django-webapp)

The purpose of developing this software is to learn how to integrate a NoSQL cloud database, specifically Firestore from Google Cloud, with the Django framework.

So, I implemented all CRUD operations for the "patients" collection. Unlike my previous project, which used SQLite, this time I've integrated Cloud Firestore for data storage.

[Software Demo Video](https://youtu.be/VLaKbfManqs)

# Cloud Database

> Cloud Firestore is a flexible, scalable database for mobile, web, and server development from Firebase and Google Cloud

## Firestore Database Structure Description

### Collections:
- Patients: Collection containing individual patient records.
  - Documents: Each document represents a unique patient record.
    - Fields:
      - firstname: (String) Stores the first name of the patient, limited to 50 characters.
      - lastname: (String) Stores the last name of the patient, limited to 50 characters.
      - email: (String) Stores the email address of the patient, ensuring uniqueness.
      - date_of_birth: (Date) Stores the date of birth of the patient.

# Development Environment

* VS Code
* Google Cloud - Firestore
* Django for Python
* Library: `pip install --upgrade firebase-admin`
* Git / GitHub
* CSS framework - Bootstrap

# Useful Websites

- [Firestore tutorial - Official site](https://firebase.google.com/docs/firestore)
- [Google Authentication - Creating a Service Account (official site)](https://cloud.google.com/docs/authentication/client-libraries)
- [Firestore with Python - Console app (Part I) - Spanish tutorial](https://www.youtube.com/watch?v=u1KZUIvI_Uo)
- [Firestore with Python - Console app (Part II) - Spanish tutorial](https://youtu.be/rGgl9Ze8nAE?si=UvMdBm5QROSwkzYG)

# Future Work

- Display a modal to confirm the patient deletion
- Set Firestore as default database in Django
- Add more fields to the patient collection
- Implement the appointment and medical history collections
