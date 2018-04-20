from django.db import models
from django.urls import reverse
from datetime import date

#Class for TrafficLight object
class TrafficLight(models.Model):
    name = models.TextField(primary_key=True)
    last_updated = models.TextField(blank=True, null=True)
    status = models.TextField(default="")
    coordinate_x = models.DecimalField(blank=True, null=True, max_digits=8, decimal_places=6)
    coordinate_y = models.DecimalField(blank=True, null=True, max_digits=8, decimal_places=6)

    def __str__(self):
        return self.name

class TrafficLightDetectors(models.Model):
    crossingname = models.CharField(max_length=25, default='')
    timestamp = models.TextField(blank=True, null=True)
    traffic_amount = models.IntegerField(blank=True, null=True, default=None)
    realiable_value = models.IntegerField(blank=True, null=True, default=None)

    def __str__(self):
        return self.timestamp