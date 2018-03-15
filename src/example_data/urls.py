# accounts/urls.py
from django.urls import path

from . import views



urlpatterns = [
    path('create/', views.TraffictLights_create, name='create'),
    path('detail/', views.TraffictLights_detail, name='detail'),
    path('', views.TraffictLights_list, name='list'),
    path('update/', views.TraffictLights_update, name='update'),
    path('delete/', views.TraffictLights_delete, name='delete'),
]

#"example_data.views.TraffictLights_home()"
#urlpatterns = [
#    path('TrafficLights/', views.SignUp.as_view(), name='signup'),
#]