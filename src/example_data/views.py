from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import TrafficLight
from .forms import TrafficLightForm


#Creates new TrafficLight object after login
def TrafficLights_create(request):
    form = TrafficLightForm(request.POST or None)

    if request.user.is_authenticated:
        if form.is_valid():
            form.save()
            return redirect('list')

            return render(request, 'trafficlights/TrafficLightForm.html', {'form': form})

    else:
        return redirect('list')

#Displays TrafficLight object details
def TrafficLights_detail(request):
    context = {
            "title": "Detail "
    }
    return render(request, "trafficlights/index.html", context)

#Lists TrafficLight objects
def TrafficLights_list(request):
    TrafficLights = TrafficLight.objects.all()
    {
        "title": "List "
    }

    return render(request, "trafficlights/index.html", {'TrafficLights': TrafficLights})

#Updates TrafficLight object after login
def TrafficLights_update(request, id):
    if request.user.is_authenticated:
        trafficlight = TrafficLight.objects.get(identifier=id)
        form = TrafficLightForm(request.POST or None, instance=TrafficLight)

        if form.is_valid():
            form.save()
            return redirect('list')

        return render(request, 'trafficlights/TrafficLightForm.html', {'form': form, 'TrafficLight':trafficlight})

    else:
        return redirect('list')    

#Removes TrafficLight object after login
def TrafficLights_delete(request, id):
    trafficlight = TrafficLight.objects.get(identifier=id)
    if request.user.is_authenticated:
        if request.method == 'POST':
            trafficlight.delete()
            print(id)
            return redirect('list')
        
        return render(request, 'trafficlights/delete-confirm.html', {'TrafficLight': trafficlight})
    else:
        return redirect('list')  