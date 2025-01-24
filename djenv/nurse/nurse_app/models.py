from django.db import models

# Create your models here.

class reg_tbl(models.Model):
    USER_TYPE_CHOICES = [
        ('admin', 'Admin'),
        ('patient', 'Patient'),
        ('nurse', 'Nurse'),
    ]
    fname=models.CharField(max_length=100)
    mob=models.IntegerField()
    email=models.EmailField()
    password=models.CharField(max_length=100)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='patient')
    def __str__(self):
        return self.fname 

class Nurse(models.Model):
    name = models.CharField(max_length=100)
    dob = models.DateField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')], default='Female')
    address = models.TextField()
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    qualification = models.TextField()
    experience = models.IntegerField(default=0)
    specialization = models.CharField(max_length=100, blank=True, null=True)
    available_days = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active')
    def __str__(self):
        return self.name

class Patient(models.Model):
    name = models.CharField(max_length=100)
    dob = models.DateField()
    gender = models.CharField(max_length=10)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    medical_history = models.TextField()
    user = models.OneToOneField(reg_tbl,on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class ServiceRequest(models.Model):
    SERVICE_TYPES = [
        ('Nursing', 'Nursing'),
        ('Physiotherapy', 'Physiotherapy'),
        ('Caregiving', 'Caregiving'),
    ]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPES)
    description = models.TextField()
    status = models.CharField(max_length=50, default='Pending')  # Approval status
    nurse_assigned = models.ForeignKey(Nurse, on_delete=models.CASCADE, null=True, blank=True)
    nurse_assignment_status = models.CharField(max_length=50, default='Not Assigned')  # Assignment status
    created_at = models.DateTimeField(auto_now_add=True)
    completestatus = models.CharField(max_length=50)
    
    def __str__(self):
        return f"Request by {self.patient.name} for {self.service_type}"