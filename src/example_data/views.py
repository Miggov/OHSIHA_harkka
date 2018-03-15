from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def TraffictLights_create(request):
    return HttpResponse("<h1>create</h1>")

def TraffictLights_detail(request):
    context = {
            "title": "Detail "
    }
    return render(request, "trafficlights/index.html", context)

def TraffictLights_list(request):
   # if request.user.is_authenticated():
    context = {
            "title": "List "
        }
  #  else:
   #     context = {
    #        "title": "Please login"
   #     }
    return render(request, "trafficlights/index.html", context)
    #return HttpResponse("<h1>list</h1>")

def TraffictLights_update(request):
    return HttpResponse("<h1>update</h1>")

def TraffictLights_delete(request):
    return HttpResponse("<h1>delete</h1>")