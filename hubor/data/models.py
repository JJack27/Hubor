from django.db import models
import django
from accounts.models import User, Bracelet
import datetime

# Create your models here.
class Data(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    bracelet = models.ForeignKey(Bracelet, on_delete=models.SET_NULL, null=True)
    time = models.DateTimeField(default=django.utils.timezone.now, null=False)
    tem = models.FloatField(default=0, null=False)
    acx = models.FloatField(default=0, null=False)
    acz = models.FloatField(default=0, null=False)
    bat = models.FloatField(default=0, null=False)
    red = models.FloatField(default=0, null=False)
    ir = models.FloatField(default=0, null=False)

class VitalSign(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    bracelet = models.ForeignKey(Bracelet, on_delete=models.SET_NULL, null=True)
    time = models.DateTimeField(default=django.utils.timezone.now, null=False)
    temp = models.FloatField(default=0, null=True)
    spo2 = models.FloatField(default=0, null=True)
    hr = models.FloatField(default=0, null=True)
    rr = models.FloatField(default=0, null=True)


class AggregatedVitalSign(models.Model):
    CHOICES = [(0,'min'), (1, 'hr'), (2, 'day'), (3, 'month')]
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    time = models.DateTimeField(defualt=django.utils.timezone.now, null=False)
    type = models.IntegerField(choices=CHOICES)
    
    # temperature
    temp_mean = models.FloatField(default=0, null=True)
    temp_mid = models.FloatField(default=0)
    temp_max = models.FloatField(default=0)
    temp_min = models.FloatField(default=0)
    temp_std = models.FloatField(default=0)

    # spo2 
    spo2_mean = models.FloatField(default=0, null=True)
    spo2_mid = models.FloatField(default=0)
    spo2_max = models.FloatField(default=0)
    spo2_min = models.FloatField(default=0)
    spo2_std = models.FloatField(default=0)

    # hr
    hr_mean = models.FloatField(default=0, null=True)
    hr_mid = models.FloatField(default=0)
    hr_max = models.FloatField(default=0)
    hr_min = models.FloatField(default=0)
    hr_std = models.FloatField(default=0)

    # rr
    rr_mean = models.FloatField(default=0, null=True)
    rr_mid = models.FloatField(default=0)
    rr_max = models.FloatField(default=0)
    rr_min = models.FloatField(default=0)
    rr_std = models.FloatField(default=0)

