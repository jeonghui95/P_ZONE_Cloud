import json
import os.path
import uuid
from typing import IO
import json

import requests

import pymysql
import requests
from django.shortcuts import render

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
        long = float(127.06139307841329)
        lat = float(37.509812901728836)
        img = request.FILES['Camera']

        # geo
        # 행정동 불러오기
        sql = "select dongcode from dong"
        cursor.execute(sql)
        dong_list = [row[0] for row in cursor.fetchall()]
        
        
        ## tmap appkey 설정 필요
        # 현 위치데이터를 dong으로 변환 및 비교
        API = "https://apis.openapi.sk.com/tmap/geo/reversegeocoding?version=1"
        payload = {"appKey": "l7xx0ffb87c22bdb45ae8facaeeb7958ad36", "lon": long, "lat": lat} 
        res = requests.get(API, params=payload)
        dongCode = int(json.loads(res.text)["addressInfo"]["legalDongCode"][5:8])
        if dongCode not in dong_list:
            print("여기는 강남구가 아님")
        else:
            print("여기는 강남구")
        print(dongCode)



        ## MODEL 서버와 통신 후 Response
        url = 'http://test-fastmodel:8000/file/store'
        upload = {'file': img}

        context = requests.post(url, files=upload).json()
        # context = requests.post(url, files=upload)
        # path= f"../../media/{save_file(img)}"
        # image = Image.open(path)
        # image.show()
        context["lat"] = lat
        context["long"] = long
        L = context["length"]
        
        
        # criteria를 기준으로 근처의 주차 금지구역 확인
        from haversine import haversine
        criteria = 100
        place_list = []
        sql = f"""SELECT c.type, c.latitude, c.longitude
                  FROM cautionzone c
                  WHERE c.dongcode={dongCode}"""
        cursor.execute(sql)
        for row in cursor.fetchall():
            distance = haversine((lat, long), (row[1], row[2]), unit="m")
            if distance < criteria:
                print(row, distance)
                place_list.append({"type": row[0], "latitude": row[1], "longitude": row[2]})
                if row[0] == "bus":
                    context["kinds"].append(4)
                    L = L+1
                elif row[0] == "fire":
                    context["kinds"].append(5)
                    L = L+1
                elif row[0] == "taxi":
                    context["kinds"].append(6)
                    L = L+1
                elif row[0] == "subway":
                    context["kinds"].append(7)
                    L = L+1
                elif row[0] == "children":
                    context["kinds"].append(8)
                    L = L+1

        #  // 주차가능구역 확인
        sql = f"""SELECT p.type, p.latitude, p.longitude
                  FROM parkingzone p
                  WHERE p.dongcode={dongCode}"""
        cursor.execute(sql)
        for row in cursor.fetchall():
            distance = haversine((lat, long), (row[1], row[2]), unit="m")
            if distance < criteria:
                print(row)
                place_list.append({"type": row[0], "latitude": row[1], "longitude": row[2]})

        context["placeList"] = place_list




        return  render(request,'result.html',context)



    ## request method가 Get일때 (Home 페이지 html 호출)
    else:
        fileuploadForm = FileUploadForm
        context = {

            'fileuploadForm': fileuploadForm,
        }
        return render(request, 'fileupload.html', context)
