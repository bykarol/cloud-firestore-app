from django.db import models

class Patient(models.Model):
    patient_firstname = models.CharField(max_length=50)
    patient_lastname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.patient_firstname} {self.patient_lastname}"

    def get_full_info(self):
        return {
            "first_name": self.patient_firstname,
            "last_name": self.patient_lastname,
            "email": self.email,
            "date_of_birth": self.date_of_birth,
            "create_at": self.patient_created_at
        }