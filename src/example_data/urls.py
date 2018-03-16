# accounts/urls.py
from django.urls import path

from .views import TrafficLights_create, TrafficLights_delete, TrafficLights_detail, TrafficLights_list, TrafficLights_update



urlpatterns = [
    path('', TrafficLights_list, name='list'),
    path('create/', TrafficLights_create, name='create'),
    path('detail/', TrafficLights_detail, name='detail'),
    path('update/<int:id>/', TrafficLights_update, name='update'),
    path('delete/<int:id>/', TrafficLights_delete, name='delete'),
]

#"example_data.views.TrafficLights_home()"
#urlpatterns = [
#    path('TrafficLights/', views.SignUp.as_view(), name='signup'),
#]