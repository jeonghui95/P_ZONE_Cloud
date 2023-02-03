import json
import os.path
import uuid
from typing import IO
import json


import haversine as haversine
import requests
from haversine import haversine

import pymysql
import requests
from django.http import HttpResponse
from django.shortcuts import render

from P_ZONE_NOTICE.settings import MARIADB
from .forms import FileUploadForm
from tempfile import NamedTemporaryFile

# def save_file(file: IO):
#     # current = os.path.abspath(__file__).split("\\")
#     # s3 업로드라고 생각해 봅시다. delete=True(기본값)이면
#     # 현재 함수가 닫히고 파일도 지워집니다.
#     UPLOAD_DIR = "./media"
#     filename = f"{str(uuid.uuid4())}.png"  # uuid로 유니크한 파일명으로 변경
#     with open(os.path.join(UPLOAD_DIR, filename), "wb") as fp:
#         fp.write(file.read())
#         return filename
#     #     tempfile = NamedTemporaryFile("wb", delete=False)
#     #     tempfile.write(file.read())
#     #     tempPath = tempfile.name.split("\\")[-1]
#     #     return tempPath

def fileUpload(request):


    host = MARIADB['default']["DB_HOST"]
    user = MARIADB['default']["DB_USER"]
    password = MARIADB['default']["DB_PASSWORD"]
    db = MARIADB['default']["DB_NAME"]

    connect = pymysql.connect(host=host, user=user, password=password, port=3306, db=db)
    cursor = connect.cursor()


    if request.method == 'POST':
        long = float(127.06139307841329)
        lat = float(37.509812901728836)
        img = request.FILES['Camera']

        # geo
        # 행정동 불러오기
        sql = "select dongcode from dong"
        cursor.execute(sql)
        dong_list = [row[0] for row in cursor.fetchall()]

        API = "https://apis.openapi.sk.com/tmap/geo/reversegeocoding?version=1"
        payload = {"appKey": "l7xx0ffb87c22bdb45ae8facaeeb7958ad36", "lon": long, "lat": lat}  ## tmap appkey 설정 필요
        res = requests.get(API, params=payload)
        dongCode = int(json.loads(res.text)["addressInfo"]["legalDongCode"][5:8])
        if dongCode not in dong_list:
            print("여기는 강남구가 아님")
        else:
            print("여기는 강남구")
        print(dongCode)

        from haversine import haversine
        criteria = 100
        place_list = []
        # 주차금지구역
        sql = f"""SELECT c.type, c.latitude, c.longitude
                  FROM cautionzone c
                  WHERE c.dongcode={dongCode}"""
        cursor.execute(sql)
        for row in cursor.fetchall():
            distance = haversine((lat, long), (row[1], row[2]), unit="m")
            if distance < criteria:
                print(row, distance)
                place_list.append({"type": row[0], "latitude": row[1], "longitude": row[2]})

        # 주차가능구역
        sql = f"""SELECT p.type, p.latitude, p.longitude
                  FROM parkingzone p
                  WHERE p.dongcode={dongCode}"""
        cursor.execute(sql)
        for row in cursor.fetchall():
            distance = haversine((lat, long), (row[1], row[2]), unit="m")
            if distance < criteria:
                print(row)
                place_list.append({"type": row[0], "latitude": row[1], "longitude": row[2]})




        # image
        # fileupload = FileUpload(
        #     title=title,
        #     content=content,
        #     imgfile=img,
        # )
        # fileupload.save()
        # return redirect('Camera_app:fileupload')


        url = 'http://test-fastmodel:8000/file/store'
        upload = {'file': img}

        context = requests.post(url,files=upload).json()
        # context = requests.post(url, files=upload)
        # path= f"../../media/{save_file(img)}"
        # image = Image.open(path)
        # image.show()
        context["lat"] = lat
        context["long"] = long
        context["placeList"] = place_list
        # m = MultipartEncoder(fields=upload)
        # headers = {'Content-Type': m.content_type}
        # res = requests.post(url, headers=headers, data=m)

        # context = json.load(res)

        return  render(request,'result.html',context)




    else:
        fileuploadForm = FileUploadForm
        context = {

            'fileuploadForm': fileuploadForm,
        }
        return render(request, 'fileupload.html', context)
# @csrf_exempt
# def imageview(request):
#     # return HttpResponse("HI")
#     if request.method == 'POST':
#         img = request.FILES["media"]
#         img = Image.open(img)
#         img.show()
#
# if "type" == "bus":
#     kinds.append(4)
#     length=length+=1
# elif "type" == "fire":
#     kinds.append(5)
#     length = length += 1
# elif "type" == "taxi":
#     kinds.append(6)
#     length = length += 1
# elif "type" == "subway":
#     kinds.append(7)
#     length = length += 1
# elif "type" == "children":
#     kinds.append(8)
#     length = length += 1
