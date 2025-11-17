from abc import ABC, abstractmethod
from datetime import datetime, timedelta, time

# -----------------------
# Abstract User Class
# -----------------------
class User(ABC):
    def __init__(self, firstname, lastname, dateOfBirth, phone, email):
        self.firstname = firstname
        self.lastname = lastname
        self.dateOfBirth = dateOfBirth
        self.phone = phone
        self.email = email
        
    def __str__(self):
        return f"{self.firstname} {self.lastname}"
    
    def __repr__(self):
        """Representation showing role for debugging."""
        return f"{self.firstname} {self.lastname} ({self.get_role()})"
    
    @abstractmethod
    def get_role(self):
        pass

# -----------------------
# Patient Class
# -----------------------
class Patient(User):
    def __init__(self, firstname, lastname, dateOfBirth, phone, email, symptoms):
        super().__init__(firstname, lastname, dateOfBirth, phone, email)
        self.symptoms = symptoms
        self.records = []
        
    def get_role(self):
        return "Patient"
    
    def choose_doctor(self, hospital_system, specialization=None):
        doctors = hospital_system.get_doctors(specialization)
        if not doctors:
            print("No doctors available with that specialization.")
            return None
        print("Available doctors:")
        for i, doc in enumerate(doctors, start=1):
            print(f"{i}. Dr. {doc.firstname} {doc.lastname} - {doc.specialization}")
        while True:
            try:
                choice = int(input("Enter the number of the doctor you want to choose: "))
                if 1 <= choice <= len(doctors):
                    return doctors[choice - 1]
                else:
                    print("Invalid choice. Try again.")
            except ValueError:
                print("Please enter a valid number.")
    
    def make_appointment(self, doctor, clinic, hospital_system, treatment, day_str):
        """Suggest available 30-min slots and schedule appointment."""
        print(f"\nScheduling appointment with Dr. {doctor.lastname} at {clinic.clinicName}...")
        
        # Parse the day
        try:
            appointment_day = datetime.strptime(day_str, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return None
        
        # Helper to parse opening hours like "8AM-5PM"
        def parse_hour(hour_str):
            hour = int(hour_str[:-2])
            if "PM" in hour_str and hour != 12:
                hour += 12
            if "AM" in hour_str and hour == 12:
                hour = 0
            return hour
        
        try:
            open_str, close_str = clinic.openingHours.split('-')
            open_hour = parse_hour(open_str.strip())
            close_hour = parse_hour(close_str.strip())
        except Exception:
            print("Invalid clinic opening hours format. Should be like '8AM-5PM'")
            return None
        
        # Generate 30-minute slots
        slots = []
        current_time = datetime.combine(appointment_day, time(open_hour, 0))
        end_time = datetime.combine(appointment_day, time(close_hour, 0))
        
        while current_time < end_time:
            if hospital_system.is_slot_available(doctor, current_time):
                slots.append(current_time)
            current_time += timedelta(minutes=30)
        
        if not slots:
            print("No available time slots for this doctor on that day.")
            return None
        
        # Show available slots
        print("Available time slots:")
        for i, slot in enumerate(slots, start=1):
            print(f"{i}. {slot.strftime('%H:%M')}")
        
        # Get user input safely
        while True:
            try:
                choice = int(input("Choose your time slot number: "))
                if 1 <= choice <= len(slots):
                    break
                else:
                    print("Invalid choice, try again.")
            except ValueError:
                print("Please enter a valid number.")
        
        selected_slot = slots[choice - 1]
        
        # Create record and store visitDate as datetime
        record = Record(self, doctor, clinic, selected_slot, treatment)
        self.records.append(record)
        doctor.records.append(record)
        hospital_system.records.append(record)
        
        print(f"Appointment scheduled for {self} with Dr. {doctor.lastname} on {selected_slot.strftime('%Y-%m-%d %H:%M')} at {clinic.clinicName}")
        return record
    
    def view_records(self):
        if not self.records:
            print(f"{self} has no records yet.")
            return
        for r in self.records:
            print(r)

# -----------------------
# Doctor Class
# -----------------------
class Doctor(User):
    def __init__(self, firstname, lastname, dateOfBirth, phone, email, specialization, licenceNumber, yearsOfExperience):
        super().__init__(firstname, lastname, dateOfBirth, phone, email)
        self.specialization = specialization
        self.licenceNumber = licenceNumber
        self.yearsOfExperience = yearsOfExperience
        self.records = []
        
    def get_role(self):
        return "Doctor"
    
    def view_appointments(self):
        if not self.records:
            print(f"Dr. {self.lastname} has no scheduled appointments.")
            return
        for r in self.records:
            print(r)

# -----------------------
# Clinic Class
# -----------------------
class Clinic:
    def __init__(self, clinicID, clinicName, address, city, province, zipcode, phone, email, openingHours, createdAt=None, updatedAt=None):
        self.clinicID = clinicID
        self.clinicName = clinicName
        self.address = address
        self.city = city
        self.province = province
        self.zipcode = zipcode
        self.phone = phone
        self.email = email
        self.openingHours = openingHours
        self.createdAt = createdAt or datetime.now()
        self.updatedAt = updatedAt or datetime.now()
        
    def __str__(self):
        return f"{self.clinicName} - at {self.city}, {self.province}"

# -----------------------
# Record Class
# -----------------------
class Record:
    def __init__(self, patient: Patient, doctor: Doctor, clinic: Clinic, visitDate: datetime, treatment):
        self.patient = patient
        self.doctor = doctor
        self.clinic = clinic
        self.visitDate = visitDate  # datetime object
        self.treatment = treatment
        
    def __str__(self):
        return f"Record: {self.patient} visited Dr. {self.doctor.lastname} at {self.clinic.clinicName} on {self.visitDate.strftime('%Y-%m-%d %H:%M')}. Treatment: {self.treatment}"

# -----------------------
# HospitalSystem Class
# -----------------------
class HospitalSystem:
    def __init__(self):
        self.records = []
        self.doctors = []

    def add_doctor(self, doctor):
        self.doctors.append(doctor)

    def get_doctors(self, specialization=None):
        if specialization:
            return [doc for doc in self.doctors if doc.specialization.lower() == specialization.lower()]
        return self.doctors

    def is_slot_available(self, doctor, visit_datetime: datetime) -> bool:
        """Check if the doctor has an appointment at the given datetime."""
        return all(record.visitDate != visit_datetime for record in doctor.records)

# -----------------------
# Example Usage
# -----------------------
if __name__ == "__main__":
    # Create hospital system
    hs = HospitalSystem()
    
    # Add doctors
    doc1 = Doctor("Alice", "Smith", "1980-06-15", "123456789", "alice@hospital.com", "Cardiology", "LIC123", 10)
    doc2 = Doctor("Bob", "Jones", "1975-09-20", "987654321", "bob@hospital.com", "Dermatology", "LIC456", 15)
    hs.add_doctor(doc1)
    hs.add_doctor(doc2)
    
    # Create clinic
    clinic = Clinic(1, "Healthy Life Clinic", "123 Main St", "Metropolis", "MetroState", "12345", "555-1111", "contact@hlclinic.com", "8AM-5PM")
    
    # Create patient
    patient = Patient("John", "Doe", "1990-01-01", "555-2222", "john@example.com", ["cough", "fever"])
    
    # Schedule appointment
    chosen_doctor = patient.choose_doctor(hs)
    if chosen_doctor:
        patient.make_appointment(chosen_doctor, clinic, hs, "General Checkup", "2025-11-18")
    
    # View patient records
    patient.view_records()
    
    # View doctor appointments
    chosen_doctor.view_appointments()
