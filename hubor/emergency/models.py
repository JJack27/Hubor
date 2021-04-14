from django.db import models
from accounts.models import User
from configurations.models import Configuration
import uuid
# Create your models here.
'''
Class holds emergency contacts relationship
'''
class EmergencyContact(models.Model):
    id = models.AutoField(primary_key = True)
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.TextField(max_length=30)
    last_name = models.TextField(max_length=30)
    phone = models.TextField(max_length=20)
    email = models.EmailField(null=True)
    relationship = models.TextField(max_length=20, default='')
    

'''
Class holds emergency events
'''
class EmergencyEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    solved = models.IntegerField(null=True, default=0)
    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)
    configuration = models.ForeignKey(Configuration, on_delete=models.SET_NULL, null=True)

'''
Class holds emergency message that have been sent
'''
class EmergencyMessage(models.Model):
    pass