from django.urls import path

app_name="Camera_app"

urlpatterns = [
    path('recog/',view, name='recog')
]