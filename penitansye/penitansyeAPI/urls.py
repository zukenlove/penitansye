from django.urls import path
from . import views

app_name = 'penitansye'
urlpatterns = [
    path('home/', views.homeView, name='home'),
    path('',views.homepage, name ="homepage"),
    path('appointment/',views.appointmentView, name ="appointment"),
    path('patient/', views.patientView, name='patient'),
    path('appointment/<int:patient_id>/', views.appointmentView, name='appointment')



] 