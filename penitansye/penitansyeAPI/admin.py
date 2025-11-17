from django.contrib import admin
from .models import  Doctor, Patient,Clinic,Record, Appointment

# Register your models here.
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Clinic)
admin.site.register(Record)
admin.site.register(Appointment)

