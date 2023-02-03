import json
import os.path
import uuid
from typing import IO
import json

import requests

import pymysql
import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect

from P_ZONE_NOTICE.settings import MARIADB
from .forms import FileUploadForm

def fileUpload(request):

    # DB requirement
    host = MARIADB['default']["DB_HOST"]
    user = MARIADB['default']["DB_USER"]
    password = MARIADB['default']["DB_PASSWORD"]
    db = MARIADB['default']["DB_NAME"]

    connect = pymysql.connect(host=host, user=user, password=password, port=3306, db=db)
    cursor = connect.cursor()



    # Request Post일때
    if request.method == 'POST':
        img = request.FILES['Camera']




        ## MODEL 서버와 통신 후 Response
        url = 'http://test-fastmodel:8000/file/store'
        upload = {'file': img}

        context = requests.post(url, files=upload).json()



        return  render(request,'result.html',context)


    ## request method가 Get일때 (Home 페이지 html 호출)
    else:
        from django.urls import reverse
        from Home.views import Index
        return reverse(Index)
        # fileuploadForm = FileUploadForm
        # context = {
        #
        #     'fileuploadForm': fileuploadForm,
        # }
        # return render(request, 'fileupload.html', context)
