from django.db import models
from django.urls import reverse
from datetime import date

#Class for TrafficLight object
class TrafficLight(models.Model):
    name = models.TextField()
    street = models.TextField(blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    identifier = models.IntegerField(default="")
    state = models.NullBooleanField(blank=True, null=True, default=None)
    last_updated = models.DateField(default=None)
    coordinate_x = models.DecimalField(blank=True, null=True, max_digits=8, decimal_places=6)
    coordinate_y = models.DecimalField(blank=True, null=True, max_digits=8, decimal_places=6)