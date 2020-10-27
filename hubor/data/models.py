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