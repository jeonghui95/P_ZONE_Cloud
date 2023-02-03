from django.shortcuts import render

# Create your views here.
import os
import pymysql
import json

from django.http import HttpResponse
from django.shortcuts import render
import requests
import json
import time

from P_ZONE_NOTICE.settings import MARIADB


def find_P_ZONE(request):

    host = MARIADB['default']["DB_HOST"]
    user = MARIADB['default']["DB_USER"]
    password = MARIADB['default']["DB_PASSWORD"]
    db = MARIADB['default']["DB_NAME"]
    # try:
    #     host =os.environ("DB_HOST")
    #     user =os.environ("DB_USER")
    #     password=os.environ("DB_PASSWORD")
    #     db=os.environ("DB_NAME")
    # except:
    #     HttpResponse("NO PARAMETER")
    #
    connect = pymysql.connect(host=host, user=user, password=password, port=3306, db=db)
    cursor = connect.cursor()
    sql = "select * from parkingpzone"
    cursor.execute(sql)
    rows = cursor.fetchall()
    # parkingzone = pd.read_csv(os.path.join(BASE_DIR,'parkingzone.csv'))

    url = f"https://apis.openapi.sk.com/tmap/routes/pedestrian?version=1"

    headers = {
        "appkey": "l7xx0ffb87c22bdb45ae8facaeeb7958ad36 ",
    }

    # 현재 위치
    longitude = float(request.GET.get('longitude'))
    latitude = float(request.GET.get('latitude'))


    minTime = 1000000000000
    for idx,row in enumerate(rows):  # row
        time.sleep(0.6)
        payload = {
            "startX": longitude,
            "startY": latitude,
            "endX": row[3], #longitude
            "endY": row[2], #
            "startName": "현위치",
            "endName": "주차장"
        }

        res = requests.post(url, json=payload, headers=headers)

        jsonObj = json.loads(res.text)

        if jsonObj["features"][0]["properties"]["totalTime"] < minTime:
            nearest = jsonObj
            minTime = jsonObj["features"][0]["properties"]["totalTime"]


    print(nearest)

    context = {
        "nearest": json.dumps(nearest)
    }
    return render(request, 'geolocation.html', context)