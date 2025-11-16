from django.urls import path
from . import views

app_name = 'Penitansye'
urlpatterns = [
    path('home/', views.homeView, name='home'),
    path('',views.homepage, name ="homepage")
] 