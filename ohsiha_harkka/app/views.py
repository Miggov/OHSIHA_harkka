from django.shortcuts import render, redirect
from rest_framework import viewsets
from .models import TrafficLight
from .serializers import TrafficLightSerializer
import requests, json



class TrafficlightstatusView(viewsets.ReadOnlyModelViewSet):
    queryset = TrafficLight.objects.all()
    serializer_class = TrafficLightSerializer

#Converts API status to English
def status(status):
    if status == "A" or status == "B" or status == "C" or status == "E" or status == "G":
        status = "red"
        return status
    elif status == "4" or status == "1" or status == "5":
        status = "green"
        return status
    elif status == "^" or status == "<" or status == ":":
        status = "yellow"
        return status
    else:
        print("Error parsing status, API returned status: ", status)
        return status

def fetch_status(request):
    main_API = 'http://trafficlights.tampere.fi/api/v1/' #url of main API
    crossingname = 'TRE906'                              #name of crossing device
    function = 'deviceState'                             #device function to be viewed
    url = main_API + function + '/' + crossingname       #generates url for fetching data
    r = requests.get(url)
    json_data = r.text
    json_obj = json.loads(json_data)
    print('API data loaded: ' + r.text)

    devices = len(json_obj["signalGroup"])             #number of trafficlights in crossing
    i=0
    while i < devices:                                 #saves data to object created in models.py
        dev_obj = TrafficLight()
        n = json_obj["signalGroup"][i]["name"].replace("_", "")
        dev_obj.name = crossingname + n
        dev_obj.status = status(json_obj["signalGroup"][i]["status"])
        dev_obj.last_updated = json_obj["timestamp"]
        dev_obj.save(update_fields=['status', 'last_updated']) #only updates dynamic fields
        i= i + 1

    objects = TrafficLight.objects.all()
    args = {'objects': objects}
    return redirect("/") #render(request, "dashboard.html", args)
