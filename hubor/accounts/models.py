from django.db import models
from django.contrib.auth.models import AbstractUser

import uuid

# Create your models here.
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(null=True, editable=True, unique=True)
    #image = models.ImageField(upload_to='profiles', editable=True, null=True)
    first_name = models.TextField(max_length=64, null=False)
    last_name = models.TextField(max_length=64, null=False)
    username = models.TextField(max_length=64, unique=True, default='user')
    phone = models.TextField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    height = models.IntegerField(null=True, default=180)
    weight = models.IntegerField(null=True, default=180)

    # 0: male
    # 1: female
    GENDERS = [(0, 'male'), (1, 'female')]
    gender = models.IntegerField(default=1, null=False, choices=GENDERS)

    # user type:
    # 0: common patient
    # 1: doctors
    # 2: admins
    USER_TYPES = [(0,'Patient'), (1, 'Doctors'), (2, 'Admins')]
    user_type = models.IntegerField(choices=USER_TYPES, default=0, null=False)

    notes = models.TextField(max_length=800, null=True, editable=True)

'''
class Patient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.TextField(max_length=64, null=False)
    last_name = models.TextField(max_length=64, null=False)
    
    date_of_birth = models.TimeField()

    # 0: male
    # 1: femail
    gender = models.IntegerField(default=0, null=False)
    notes = models.TextFiled(max_length=800, null=True, editable=True)
'''

class Bracelet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    mac_addr = models.TextField(max_length=17, null=False)


'''
Represents the relationship between doctors and patients.
'''
class TakeCareOf(models.Model):
    id = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor')
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient')
    since = models.DateTimeField(auto_now_add=True)

'''
Status of patients
'''
class PatientStatus(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='status')
    
    RISK_LEVELS = [(0,'LOW'), (1, 'MID'), (2, 'HIGH')]
    risk = models.IntegerField(default=0, null=False, choices=RISK_LEVELS)


'''
Health Care Facilities
'''
class Facilities(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.TextField(max_length=100)
    address = models.TextField(max_length=150)
    phone = models.TextField(max_length=20)
    description = models.TextField(max_length=400, null=True)

'''
Relationship between facilities and users
'''
class BelongsToFacilities(models.Model):
    id = models.AutoField(primary_key=True)
    since = models.DateTimeField(auto_now_add=True)
    facility = models.ForeignKey(Facilities, on_delete=models.CASCADE, related_name='having')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='belongsto')