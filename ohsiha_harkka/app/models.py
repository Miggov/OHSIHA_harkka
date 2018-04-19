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
    detector = models.CharField(max_length=25, default='')
    device = models.CharField(max_length=25, default='')
    traffic_amount = models.IntegerField(blank=True, null=True, default=None)
    realiable_value = models.IntegerField(blank=True, null=True, default=None)
    congestion_count = models.IntegerField(blank=True, null=True, default=None)
    queue_length = models.IntegerField(blank=True, null=True, default=None)
    vehicle_count = models.IntegerField(blank=True, null=True,default=None)
    wait_time_max = models.FloatField(blank=True, null=True, default=None)
    wait_time_avg = models.FloatField(blank=True, null=True, default=None)
    latitude = models.FloatField(blank=True, null=True, default=None)
    longitude = models.FloatField(blank=True, null=True, default=None)
    street_name = models.CharField(max_length=100, blank=True, null=True, default=None)

    def __str__(self):
        return self.detector
