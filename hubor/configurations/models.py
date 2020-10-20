from django.db import models

# Create your models here.
class Configuration(models.Model):
    NAME_CHOICES = (
        ("TEM", "tem"),
        ("ACX", "acx"),
        ("ACZ", "acz"),
        ("BAT", "bat"),
        ("RED", "red"),
        ("IR", "ir")
    )

    COMPARE_CHOICES = (
        (0, "greater"),
        (1, "less"),
        (2, "within")
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(null=False, max_length=3, choices=NAME_CHOICES, default="TEM")
    
    # Compare methods: 0-greater, 1-less, 2-within
    compare = models.IntegerField(null=False, choices=COMPARE_CHOICES, default=0)
    
    # Range for comparison, default is the min/max of the integer
    range_min = models.FloatField(null = False, default=0x80000000)
    range_max = models.FloatField(null = False, default=0x7fffffff)

    # In the unit of seconds
    duration = models.IntegerField(null = False, default = 0)
