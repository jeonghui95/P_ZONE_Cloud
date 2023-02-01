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
        long = float(request.POST.get('long'))
        lat = float(request.POST.get('lat'))
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
        import numpy as np
        import base64
        import cv2
        cv_img = cv2.imdecode(np.frombuffer(img.read(), np.uint8), cv2.IMREAD_UNCHANGED)
        is_success, img_buf_arr = cv2.imencode(".png", cv_img)
        encoded_img = base64.b64encode(img_buf_arr.tobytes()) # base64로 변환
        uri = f"data:image/png;base64,{str(encoded_img)[2:-2]}"

        # fileupload = FileUpload(
        #     title=title,
        #     content=content,
        #     imgfile=img,
        # )
        # fileupload.save()
        # return redirect('Camera_app:fileupload')


        url = 'http://fastmodel:8000/file/store'
        upload = {'file': img}

        # context = requests.post(url,files=upload).json()
        # context = requests.post(url, files=upload)
        # path= f"../../media/{save_file(img)}"
        # image = Image.open(path)
        # image.show()
        context=dict()
        context["lat"] = lat
        context["long"] = long
        context['imgpath'] = uri
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