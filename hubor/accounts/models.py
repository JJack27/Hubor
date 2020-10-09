from django.db import models
from django.contrib.auth.models import AbstractUser

import uuid

# Create your models here.
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(null=False, editable=True, unique=True)
    #image = models.ImageField(upload_to='profiles', editable=True, null=True)
    first_name = models.TextField(max_length=64, null=False)
    last_name = models.TextField(max_length=64, null=False)
    username = models.TextField(max_length=64, unique=True, default='user')
    phone = models.TextField(max_length=20, unique=True)
    date_of_birth = models.TimeField()

    # 0: male
    # 1: femail
    gender = models.IntegerField(default=1, null=False)

    # user type:
    # 0: common patient
    # 1: doctors
    # 2: admins
    user_type = models.IntegerField(default=0)

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
