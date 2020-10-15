from django.db import models
from accounts.models import User, Bracelet

# Create your models here.
class Data(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    bracelet = models.ForeignKey(Bracelet, on_delete=models.SET_NULL, null=True)
    time = models.DateTimeField(auto_now_add=True, null=False)
    tem = models.FloatField(default=0, null=False)
    acx = models.FloatField(default=0, null=False)
    acz = models.FloatField(default=0, null=False)
    bat = models.FloatField(default=0, null=False)
    red = models.FloatField(default=0, null=False)
    ir = models.FloatField(default=0, null=False)