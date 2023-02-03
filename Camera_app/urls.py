
from django.urls import path
from .views import *

app_name="Camera_app"

urlpatterns = [
	path('fileupload/', fileUpload, name="fileupload"),
	# path('photo/',forbidden_location,name="photo")
]


