from django.shortcuts import render, redirect
from app.models import TrafficLight
from django import template

@register.assignment_tag
def drawMap():
    map_points = TrafficLight.objects.all()
    print map_points
    pointlist = {}
    for point in map_points
        pointlist.append point
    print(pointlist)
    return pointlist
