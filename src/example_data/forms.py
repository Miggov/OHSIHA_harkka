from django import forms
from .models import TrafficLight

class TrafficLightForm(forms.ModelForm):
    class Meta:
        model = TrafficLight
        fields = ['name', 'street', 'number', 'identifier', 'last_updated', 'coordinate_x', 'coordinate_y']