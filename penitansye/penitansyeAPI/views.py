from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Appointment, Patient
from .forms import AppointmentForm, PatientForm
# Create your views here.

def homepage(request):
    context = {
        'homepage':"this my first page",
        }
    return render(request, 'penitansyeAPI/index.html',context)


# rest framework views
@api_view(['GET'])
def homeView(request):
    return Response({'message':"Welcome to my homepage"}, status=status.HTTP_200_OK)

def appointmentView(request, patient_id=None):
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            if Appointment.objects.filter(
                doctor=appointment.doctor,
                visit_date=appointment.visit_date
            ).exists():
                messages.error(request, "This time slot is already taken.")
                return render(request, "penitansyeAPI/appointment_form.html", {"form": form})
            appointment.save()
            messages.success(request, "Appointment successfully created!")
            return redirect("appointments_list")
    else:
        if patient_id:
            form = AppointmentForm(initial={'patient': patient_id})
        else:
            form = AppointmentForm()

    return render(request, "penitansyeAPI/appointment_form.html", {"form": form})


def patientView(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            new_patient = form.save()
            messages.success(request, "Patient added successfully!")
            # Redirect to appointment page with newly created patient
            return redirect('penitansye:appointment', patient_id=new_patient.id)
    else:
        form = PatientForm()

    return render(request, 'penitansyeAPI/patient_form.html', {'form': form})
