from django.shortcuts import render, redirect
from rest_framework import viewsets
from .models import TrafficLight, TrafficLightDetectors
from .serializers import TrafficLightSerializer, TrafficAmountSerializer
from datetime import datetime as dt
from threading import Timer
import requests, json, time, datetime, threading



class TrafficlightstatusView(viewsets.ReadOnlyModelViewSet):
    queryset = TrafficLight.objects.all()
    serializer_class = TrafficLightSerializer

class TrafficAmountView(viewsets.ReadOnlyModelViewSet):
    queryset = TrafficLightDetectors.objects.all()
    serializer_class = TrafficAmountSerializer

#Converts API status to English
def status(status):
    if status == "A" or status == "B" or status == "C" or status == "E" or status == "G" or status == "H":
        status = "red"
        return status
    elif status == "4" or status == "1" or status == "5" or status == "0":
        status = "green"
        return status
    elif status == "^" or status == "<" or status == ":":
        status = "yellow"
        return status
    else:
        print("Error parsing status, API returned status: ", status)
        return status

def fetch_trafficdata(): #Loads traffic amount every 15 minutes
    main_API = 'http://trafficlights.tampere.fi/api/v1/' #url of main API
    crossingname = 'TRE906'                              #name of crossing device
    function = 'trafficAmount'                             #device function to be viewed
    url = main_API + function + '/' + crossingname       #generates url for fetching data
    r = requests.get(url)
    json_data = r.text
    json_obj = json.loads(json_data)

    devices = len(json_obj["results"])
    trafficAmount = 0
    reliableValue = 0
    i=0
    while i < devices:
        tramount = json_obj["results"][i]["trafficAmount"]
        if tramount == None:
            trafficAmount += 0
        else:
            trafficAmount += tramount 
        rvalue = json_obj["results"][i]["reliabValue"]
        if rvalue == None:
            reliableValue += 0
        else:
            reliableValue += rvalue
        i = i + 1
    device_object = TrafficLightDetectors()
    device_object.crossingname = crossingname
    device_object.timestamp = datetime.datetime.strptime(json_obj["responseTs"], '%Y-%m-%dT%H:%M:%S+%f:00')
    device_object.traffic_amount = trafficAmount
    device_object.realiable_value = reliableValue
    device_object.save()
    print("Trafficdata loaded ", time.ctime())
    threading.Timer(900, fetch_trafficdata).start()
    return

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
    return redirect("/")

def truncate_trafficdata():
    TrafficLightDetectors.objects.all().delete()
    print("Trafficdata truncated ", time.ctime())

def timer():
    x=dt.today()
    y=x.replace(day=x.day+1, hour=1, minute=0, second=0, microsecond=0)
    delta_t=y-x

    secs=delta_t.seconds+1

    t = Timer(secs, truncate_trafficdata())
    t.start()


timer()
fetch_trafficdata()