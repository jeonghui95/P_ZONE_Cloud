# from P_ZONE_NOTICE.settings import MARIADB
# import pymysql
# import json
# import requests
# from haversine import haversine
#
# long = 127.0507571
# lat = 37.5030042
#
#
# host = MARIADB['default']["DB_HOST"]
# user = MARIADB['default']["DB_USER"]
# password = MARIADB['default']["DB_PASSWORD"]
# db = MARIADB['default']["DB_NAME"]
# connect = pymysql.connect(host=host, user=user, password=password, port=3306, db=db)
# cursor = connect.cursor()
#
#
# sql = "select dongcode from dong"
# cursor.execute(sql)
# dong_list = [row[0] for row in cursor.fetchall()]
#
#
# API = "https://apis.openapi.sk.com/tmap/geo/reversegeocoding?version=1"
# payload = {"appKey": "l7xx0ffb87c22bdb45ae8facaeeb7958ad36", "lon": long, "lat": lat} ## tmap appkey 설정 필요
# res = requests.get(API, params=payload)
# dongCode = int(json.loads(res.text)["addressInfo"]["legalDongCode"][5:8])
# if dongCode not in dong_list:
#     print("여기는 강남구가 아님")
# else:
#     print("여기는 강남구")
# print(dongCode)
#
# criteria = 100
# # 주차금지구역
# sql = f"""SELECT c.type, c.latitude, c.longitude
#           FROM cautionzone c
#           WHERE c.dongcode={dongCode}"""
# cursor.execute(sql)
# for row in cursor.fetchall():
#     distance = haversine((lat, long), (row[1], row[2]), unit="m")
#     if distance < criteria:
#         print(row, distance)
#
#
# # 주차가능구역
# sql = f"""SELECT p.type, p.latitude, p.longitude
#           FROM parkingzone p
#           WHERE p.dongcode={dongCode}"""
# cursor.execute(sql)
# for row in cursor.fetchall():
#     distance = haversine((lat, long), (row[1], row[2]), unit="m")
#     if distance < criteria:
#         print(row)


import numpy as np
import base64
import cv2

cv_img = cv2.imdecode(np.frombuffer(img.read(), np.uint8), cv2.IMREAD_UNCHANGED)
is_success, img_buf_arr = cv2.imencode(".png", cv_img)
encoded_img = base64.b64encode(img_buf_arr.tobytes()) # base64로 변환
uri = f"data:image/png;base64,{str(encoded_img)[2:-2]}"