Mikko Vaaranmäki
# Harjoitustyö vaihe 4: Datan visualisointi

Harjoitustyön neljännessä vaiheessa keskityin lisädatan hankintaan ja visualisointiin. Hain Tampereen liikennevalorajapinnasta myös tietoja liikennevirrasta.

## Kertaus käytössä olevista teknologioista ja y
-Python 3.6.4
-Django 2.0.4
-Django REST framework
-Google Charts
-Leaflet.js
-Virtualenv
-SQLite
-VisualStudio Code
-Postman

## Työn eteneminen
Lisädatan hakeminen kantaan oli melko pieni osa työtä, ja se onnistui melko yksinkertaisella funktiolla. Haluan tarkastella kokonaisliikennevirtaa risteyksessä ajan funktiona, joten summasin yksittäisten tunnistimien arvot jo tässä vaiheessa.
```
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
        trafficAmount += json_obj["results"][i]["trafficAmount"]
        reliableValue += json_obj["results"][i]["reliabValue"]
        i = i + 1
    device_object = TrafficLightDetectors()
    device_object.crossingname = crossingname
    device_object.timestamp = datetime.datetime.strptime(json_obj["responseTs"], '%Y-%m-%dT%H:%M:%S+%f:00')
    device_object.traffic_amount = trafficAmount
    device_object.realiable_value = reliableValue
    device_object.save()
    print(time.ctime())
    threading.Timer(900, fetch_trafficdata).start()
    return
```
Otin käyttöön myös oman REST API:n [Django REST Frameworkia](http://www.django-rest-framework.org/#quickstart) hyödyntäen. Hyödynnän rajapintaa paitsi datan esittämiseen, myös (mikäli aikataulu vaan mitenkään riittää) Telegram-chatbotin tekemiseen. Rajapinnan määrittäminen on melko yksinkertaista ohjeita noudattaen:
#### Serializers.py
```
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

```
#### Rajapintaan liittyvät viewit
```
class TrafficlightstatusView(viewsets.ReadOnlyModelViewSet):
    queryset = TrafficLight.objects.all()
    serializer_class = TrafficLightSerializer

class TrafficAmountView(viewsets.ReadOnlyModelViewSet):
    queryset = TrafficLightDetectors.objects.all()
    serializer_class = TrafficAmountSerializer
```
#### ...ja urls.py
```
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from .views import fetch_status, TrafficlightstatusView, TrafficAmountView
from django.conf.urls import url, include
from rest_framework import routers

router = routers.DefaultRouter()
router.register('TrafficLights', TrafficlightstatusView)
router.register('TrafficAmount', TrafficAmountView)

urlpatterns = [
    path('', include(router.urls)),
    path('update/', fetch_status, name='update'), # update TrafficLight status
]
```
#### Datan haku kartalle
Yhdistin Leaflet.js kirjaston Google mapsin karttapohjaan lähinnä omien mieltymysten takia. Osoittimena kartalla käytin L.circle tyyppistä osoitinta, koska ymmärtääkseni ainoastaan tälle saa valittua värin.
```
    <div id="mapid">
      <script>
        function load_data() {
          fetch('http://127.0.0.1:8000/app/TrafficLights')
            .then(res => res.json())
            .then(data => TrafficLights = data)
            .then(function(TrafficLights){
              for (let i=0;i<TrafficLights.length;i++){
                let status = TrafficLights[i]['status'];
                let lat = parseFloat(TrafficLights[i]['coordinate_x']);
                let lon = parseFloat(TrafficLights[i]['coordinate_y']);
                let circle = L.circle([lat, lon], {
                  color: status,
                  fillOpacity: 1,
                  radius: 5}).addTo(mymap);
              }
            })
        }

        var mymap = L.map('mapid').setView([61.448357, 23.854091], 17); //Setting default centerplace for the map

        // Loading gmaps layer
        googleStreets = L.tileLayer('http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',{ 
          maxZoom: 20,
          subdomains:['mt0','mt1','mt2','mt3']
      }).addTo(mymap);

    
        mymap.on('moveend', load_data);
        load_data();
      </script>
    </div>
    
```

Dashboardilla näkyy tällä hetkellä siis liikennemäärän muutos sekä liikennevalojen statukset kartalla. Kartta päivittyy aina sitä liikutettaessa ja liikennetiedot 15 min välein. 

![alt text](https://lh3.googleusercontent.com/VAN_OHERw86mi_gBNt6363kSiAcLWu95a5xIX6XVGycke72Qvv64Znnj87uXGjB0Np_LPM0JcszJriCZ9I48kVxdgLTXHmYbZgbf0t4phe3GXvCRy-Z_YAi6bijnmsj2Esgl4iHB3dXg4yOe6dLLK73RmC77FmjMnxK9XoMN0qUcnoNMsJXuY79AzFtp5qzPz84Gd_-_Pj6o-P5N1ko_bvpH_pNT1UGRkEZTgOfsm0JkHGspCR2pdkccqPCnlzP1JnyHgU3hssLOyuTK53amS7Cixl2ol4tqgCqXr2fVxQ8fIbqriXu53U_rnTRG2hzByfJdOkHHrs4JWV8tnBqyQ-eiWSFxbs3Q-Fvv8595RF87zXAv5pYllx1NjVekVwwlWk4ReIJpfChS_w7Ker-iwyosnkruKSNT7aAoEp2hiMh6E41zIpLssQq1V_jCfWzDooENjFZxOIfLSLZrSKIqE5k-rc5NY1VC5pfcRNGl0yi-smv3B4dVy_qeO7dbE0Flmtf5oy7zcva1eNZ1m9IbGgpm5OHnYQ_rekBwYP2AbkcseIBVAH0t_rLOflaRSimcbdtWN1sqg1qnJ22SrxKJEZ4t5Uf89VTXczTD4XQ=w1062-h608-no)

## Helpot ja hankalat
Vaikeimmaksi osoittautui jälleen kerran datan pyörittely javascript muotoisen visualisoinnin ymmärrettäväksi, kun omat javascriptitaidot ovat aika nollassa. Jonkin verran tätä prosessia suoraviivaisti mielestäni REST rajapinnan käyttöönotto, joka oli lopulta melko suoraviivainen prosessi hyvien ohjeiden ansiosta. Tässä kohtaa tosin tapoja oli useampia ja oikean tavan valinta hieman hidasti tahtia. Aikaa paloi jälleen kryptisen rajapinnan selvittelyyn eikä tulkintani aivan välttämättä ole oikein, mutta ehkä on kuitenkin paras siirtyä eteenpäin, jotta harkka tulisi joskus valmiiksikin. Lopuksi vielä ote omasta tulkinnastani rajapinnan palauttamien statuksien tulkkaamisessa sille varalle että joku muukin taistelee saman ongelman kanssa:
```
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
```