from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email, firstname, lastname, date_of_birth, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, firstname=firstname, lastname=lastname, date_of_birth=date_of_birth, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, firstname, lastname, date_of_birth, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, firstname, lastname, date_of_birth, password, **extra_fields)


class User(AbstractBaseUser):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'lastname', 'date_of_birth']

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.firstname} {self.lastname}"


class Patient(User):
    emmergencycontactname = models.CharField(max_length=200)
    emmergencycontactphone = models.CharField(max_length=15)
    bloodType = models.CharField(max_length=50)
    Allergies = models.CharField(max_length= 50)
    symptoms = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Patient - {self.firstname} {self.lastname}"   


class Doctor(User):
    specialization = models.CharField(max_length=50)
    licence_number = models.CharField(max_length=50)
    years_of_experience = models.PositiveIntegerField()


class Clinic(models.Model):
    clinic_name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    province = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    opening_hours = models.CharField(max_length=50)  # e.g., "8AM-5PM"
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.clinic_name} - {self.city}"


class Record(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="records")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="records")
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name="records")
    visit_date = models.DateTimeField()
    treatment = models.TextField()

    def __str__(self):
        return f"Record: {self.patient} visited Dr. {self.doctor.lastname} at {self.clinic.clinic_name} on {self.visit_date.strftime('%Y-%m-%d %H:%M')}"


from django.db import models
from django.utils import timezone

class Appointment(models.Model):
    patient = models.ForeignKey(
        'Patient',
        on_delete=models.CASCADE,
        related_name='appointments'
    )
    doctor = models.ForeignKey(
        'Doctor',
        on_delete=models.CASCADE,
        related_name='appointments'
    )
    clinic = models.ForeignKey(
        'Clinic',
        on_delete=models.CASCADE,
        related_name='appointments'
    )

    visit_date = models.DateTimeField()   # exact date + time
    treatment = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['visit_date']
        unique_together = ('doctor', 'visit_date')  
        # Prevent double-booking a doctor

    def __str__(self):
        return (
            f"Appointment: {self.patient.firstname} {self.patient.lastname} "
            f"with Dr. {self.doctor.lastname} at {self.clinic.clinic_name} "
            f"on {self.visit_date.strftime('%Y-%m-%d %H:%M')}"
        )
