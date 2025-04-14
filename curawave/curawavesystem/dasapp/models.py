from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import datetime

class CustomUser(AbstractUser):
    USER = {
        (1, 'admin'),
        (2, 'doc'),
        (3, 'patient'),
    }
    user_type = models.CharField(choices=USER, max_length=50, default=1)
    profile_pic = models.ImageField(upload_to='profile_pic/', null=True, blank=True)

    def get_profile_pic_url(self):
        if self.profile_pic:
            return self.profile_pic.url
        return "/static/img/default-profile.jpg"

class Specialization(models.Model):
    sname = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.sname
   

class DoctorReg(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
   
    mobilenumber = models.CharField(max_length=11)
    specialization_id = models.ForeignKey(Specialization, on_delete=models.CASCADE)
    regdate_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.admin:
            return f"{self.admin.first_name} {self.admin.last_name} - {self.mobilenumber}"
        else:
            return f"User not associated - {self.mobilenumber}"

class Patient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=11)
    address = models.TextField(blank=True)
    blood_group = models.CharField(max_length=5, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class AppointmentManager(models.Manager):
    def get_patient_appointments(self, patient):
        return self.filter(patient=patient).order_by('-created_at')
        
    def get_doctor_appointments(self, doctor):
        return self.filter(doctor_id=doctor).order_by('-created_at')
        
    def get_pending_appointments(self, doctor):
        return self.filter(doctor_id=doctor, status='0').order_by('date_of_appointment', 'time_of_appointment')
        
    def get_approved_appointments(self, doctor):
        return self.filter(doctor_id=doctor, status='Approved').order_by('date_of_appointment', 'time_of_appointment')
        
    def get_completed_appointments(self, doctor):
        return self.filter(doctor_id=doctor, status='Completed').order_by('-date_of_appointment', '-time_of_appointment')
        
    def get_cancelled_appointments(self, doctor):
        return self.filter(doctor_id=doctor, status='Cancelled').order_by('-created_at')

class Appointment(models.Model):
    appointmentnumber = models.CharField(max_length=255)
    fullname = models.CharField(max_length=255)
    email = models.EmailField()
    mobilenumber = models.CharField(max_length=255)
    doctor_id = models.ForeignKey(DoctorReg, on_delete=models.CASCADE)
    patient = models.ForeignKey('Patient', on_delete=models.SET_NULL, null=True, blank=True)
    date_of_appointment = models.DateField()
    time_of_appointment = models.TimeField()
    additional_msg = models.TextField(null=True, blank=True)
    remark = models.TextField(null=True, blank=True)
    prescription = models.TextField(null=True, blank=True)
    recommendedtest = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AppointmentManager()

    def __str__(self):
        return f"{self.fullname} - {self.appointmentnumber}"

    def is_upcoming(self):
        now = timezone.now()
        appointment_datetime = datetime.combine(self.date_of_appointment, self.time_of_appointment)
        return appointment_datetime > now

    def is_past(self):
        now = timezone.now()
        appointment_datetime = datetime.combine(self.date_of_appointment, self.time_of_appointment)
        return appointment_datetime < now

    def can_cancel(self):
        return self.status == '0' and self.is_upcoming()

class Page(models.Model):
    pagetitle = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    aboutus = models.TextField()
    email = models.EmailField(max_length=200)
    mobilenumber = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.pagetitle

