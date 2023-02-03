from django.contrib.auth import admin
from django.urls import path, include

from geolocation.views import find_P_ZONE

app_name="geolocation_app"

urlpatterns = [
    path('/',find_P_ZONE, name= "geolocation")
]
