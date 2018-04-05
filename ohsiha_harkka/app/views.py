from django.shortcuts import render
from .models import TrafficLight
import requests, json


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
        dev_obj.status = json_obj["signalGroup"][i]["status"]
        dev_obj.last_updated = json_obj["timestamp"]
        dev_obj.save()
        i= i + 1

    objects = TrafficLight.objects.all()
    args = {'objects': objects}
    return render(request, "dashboard.html", args)

