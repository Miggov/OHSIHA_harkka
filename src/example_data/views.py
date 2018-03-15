from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import TrafficLight
from .forms import TrafficLightForm

# Create your views here.

def TrafficLights_create(request):
    form = TrafficLightForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('TrafficLights_list')

    return render(request, 'trafficlights/TrafficLightForm.html', {'form': form})

def TrafficLights_detail(request):
    context = {
            "title": "Detail "
    }
    return render(request, "trafficlights/index.html", context)

def TrafficLights_list(request):
   # if request.user.is_authenticated():
    TrafficLights = TrafficLight.objects.all()
    {
            "title": "List "
        }
  #  else:
   #     Trafficlights = {
    #        "title": "Please login"
   #     }
    return render(request, "trafficlights/index.html", {'TrafficLights': TrafficLights})
    #return HttpResponse("<h1>list</h1>")

def TrafficLights_update(request):
    return HttpResponse("<h1>update</h1>")

def TrafficLights_delete(request):
    return HttpResponse("<h1>delete</h1>")