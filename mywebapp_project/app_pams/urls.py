from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('newpatient/', views.newpatient, name='newpatient'),
    path('updatepatient/<str:patient_id>/', views.updatepatient, name='updatepatient'),
    path('deletepatient/<str:patient_id>/', views.deletepatient, name='deletepatient'),
]
