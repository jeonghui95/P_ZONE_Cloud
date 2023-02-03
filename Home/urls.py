from django.urls import path

from Home.views import Index

app_name="Home_app"

urlpatterns = [
    path('',Index, name= "Home")
]