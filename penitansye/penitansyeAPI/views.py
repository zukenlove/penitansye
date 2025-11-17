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

            
def appointmentView(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)

        if form.is_valid():
            appointment = form.save(commit=False)

            # Check if the doctor is already booked at this time
            if Appointment.objects.filter(
                doctor=appointment.doctor,
                visit_date=appointment.visit_date
            ).exists():
                messages.error(request, "This time slot is already taken.")
                return render(request, "penitansyeAPI/appointment_form.html", {"form": form})

            try:
                appointment.save()
                messages.success(request, "Appointment successfully created!")
                return redirect("appointments_list")  # change to your route
                
            except IntegrityError:
                messages.error(request, "Doctor is already booked at this time.")
                return render(request, "penitansyeAPI/appointment_form.html", {"form": form})

    else:
        form = AppointmentForm()

    return render(request, "penitansyeAPI/appointment_form.html", {"form": form})

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PatientForm


def patientView(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Patient added successfully!")
            return redirect('appointment')

            # return redirect('appointment', patient_id=new_patient.id)
    else:
        form = PatientForm()

    return render(request, 'penitansyeAPI/patient_form.html', {'form': form})
