from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def TraffictLights_home(request):
    return HttpResponse("<h1>Hello_world</h1>")