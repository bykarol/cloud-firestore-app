from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('newpatient/', views.newpatient, name='newpatient'),
     path('updatepatient/', views.updatepatient, name='updatepatient'),
      path('deletepatient/', views.deletepatient, name='deletepatient'),
]
