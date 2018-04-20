from rest_framework import serializers
from app.models import TrafficLight, TrafficLightDetectors


class TrafficLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrafficLight
        fields = ('name', 'last_updated', 'status', 'coordinate_x', 'coordinate_y')

class TrafficAmountSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrafficLightDetectors
        fields = ('crossingname', 'timestamp', 'traffic_amount', 'realiable_value')

    