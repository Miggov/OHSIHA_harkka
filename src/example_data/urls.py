# accounts/urls.py
from django.urls import path

from . import views


urlpatterns = [
    path('home/', views.TraffictLights_home, name='home'),
]

#"example_data.views.TraffictLights_home()"
#urlpatterns = [
#    path('TrafficLights/', views.SignUp.as_view(), name='signup'),
#]