from rest_framework import serializers
from app.models import TrafficLight


class TrafficLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrafficLight
        fields = ('name', 'last_updated', 'status', 'coordinate_x', 'coordinate_y')

    