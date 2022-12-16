from urllib.parse import urlencode, unquote, quote_plus
import urllib
import pandas as pd
from django.shortcuts import render
import googlemaps
import requests # HTTP 요청을 보내는 모듈
import datetime # 날짜시간 모듈
import math
import json  # json 파일 파싱하여 데이터 읽는 모듈
from urllib.request import urlopen
import datetime # 날짜시간 모듈
from datetime import date, datetime, timedelta # 현재 날짜 외의 날짜 구하기 위한 모듈

gmaps = googlemaps.Client(key="AIzaSyBTmrYMwJez4u2jczuI3Fhpj1SLrMxRDnU")
url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
'''
실황정보를 조회하기 위해 발표일자, 발표시각, 예보지점 X 좌표, 예보지점 Y 좌표의 조회 조건으로
자료구분코드, 실황값, 발표일자, 발표시각, 예보지점 X 좌표, 예보지점 Y 좌표의 정보를 조회하는 기능
'''
service_key = "1HyN5CpAcCICizuwcx%2FW0DBWu3icqrH%2BUNPl3PiC9HxqEyn7764WVIf9sLA4ei%2FGNKHVCHbSxi%2B63Py7VqwnMg%3D%3D"
serviceKeyDecoded = unquote(service_key, 'UTF-8')
now = datetime.now()
print("지금은", now.year, "년", now.month, "월", now.day, "일", now.hour, "시", now.minute, "분", now.second, "초입니다.")
today = datetime.today() # 현재 지역 날짜 반환
today_date = today.strftime("%Y%m%d") # 오늘의 날짜 (연도/월/일 반환)
print('오늘의 날짜는', today_date)
# 어제
yesterday = date.today() - timedelta(days=1)
yesterday_date=yesterday.strftime('%Y%m%d')
print('어제의 날짜는', yesterday_date)
# 위치정보 거부 시 기본 좌표값 : 강남구
nx = "61"
ny = "126"


def main(request):
    nx1 = ""
    ny1 = ""

    if request.method == 'POST':
        params = {
            'serviceKey': "1HyN5CpAcCICizuwcx%2FW0DBWu3icqrH%2BUNPl3PiC9HxqEyn7764WVIf9sLA4ei%2FGNKHVCHbSxi%2B63Py7VqwnMg%3D%3D",
            'pageNo': '1', 'numOfRows': '1000', 'dataType': 'XML',
            'base_date': '20210628', 'base_time': '0500', 'nx': nx1, 'ny': ny1}
        response = requests.get(url, params=params)
        print("------------------------------")
        print(response.content)
        background = "/static/videos/rainy.mp4"
        grid(float(request.POST.get('startLat')), float(request.POST.get('startLon')))
        # 1일 총 8번 데이터가 업데이트 된다.(0200, 0500, 0800, 1100, 1400, 1700, 2000, 2300)
        # 현재 api를 가져오려는 시점의 이전 시각에 업데이트된 데이터를 base_time, base_date로 설정
        if now.hour < 2 or (now.hour == 2 and now.minute <= 10):  # 0시~2시 10분 사이
            base_date = yesterday_date  # 구하고자 하는 날짜가 어제의 날짜
            base_time = "2300"
        elif now.hour < 5 or (now.hour == 5 and now.minute <= 10):  # 2시 11분~5시 10분 사이
            base_date = today_date
            base_time = "0200"
        elif now.hour < 8 or (now.hour == 8 and now.minute <= 10):  # 5시 11분~8시 10분 사이
            base_date = today_date
            base_time = "0500"
        elif now.hour <= 11 or now.minute <= 10:  # 8시 11분~11시 10분 사이
            base_date = today_date
            base_time = "0800"
        elif now.hour < 14 or (now.hour == 14 and now.minute <= 10):  # 11시 11분~14시 10분 사이
            base_date = today_date
            base_time = "1100"
        elif now.hour < 17 or (now.hour == 17 and now.minute <= 10):  # 14시 11분~17시 10분 사이
            base_date = today_date
            base_time = "1400"
        elif now.hour < 20 or (now.hour == 20 and now.minute <= 10):  # 17시 11분~20시 10분 사이
            base_date = today_date
            base_time = "1700"
        elif now.hour < 23 or (now.hour == 23 and now.minute <= 10):  # 20시 11분~23시 10분 사이
            base_date = today_date
            base_time = "2000"
        else:  # 23시 11분~23시 59분
            base_date = today_date
            base_time = "2300"
        payload = "serviceKey=" + service_key + "&" + \
                  "dataType=json" + "&" + \
                  "base_date=" + base_date + "&" + \
                  "base_time=" + base_time + "&" + \
                  "nx=" + nx1 + "&" + \
                  "ny=" + ny1
        # 값 요청 (웹 브라우저 서버에서 요청 - url주소와 )
        res = requests.get(url + payload)
        items = res.json().get('response').get('body').get('items')
        data = dict()
        data['date'] = base_date
        weather_data = dict()
        '''
        for item in items['item']:
            # 기온
            if item['category'] == 'T3H':
                weather_data['tmp'] = item['fcstValue']

            # 기상상태
            if item['category'] == 'PTY':

                weather_code = item['fcstValue']

                if weather_code == '1':
                    weather_state = '비'
                elif weather_code == '2':
                    weather_state = '비/눈'
                elif weather_code == '3':
                    weather_state = '눈'
                elif weather_code == '4':
                    weather_state = '소나기'
                else:
                    weather_state = '없음'
                weather_data['code'] = weather_code
                weather_data['state'] = weather_state
        '''
        data['weather'] = weather_data
        for i in data:
            print(data[i])
        # ex) {'code': '0', 'state': '없음', 'tmp': '17'} # 17도 / 기상 이상 없음
        context = {
            'background': background,
        }
        return render(request, 'mainapp/main.html', context)
    else:
        # 날씨 정보 차단시 default 값 출력.
        background = "/static/videos/rainy.mp4"
        context = {
            'background': background
        }
        return render(request, 'mainapp/main.html', context)


def checkin(request):
    context = {
    }
    return render(request, 'mainapp/checkin.html', context)


# 위도 경도 기상청 xy 좌표로 변환
def grid(v1, v2):
    RE = 6371.00877  # 지구 반경(km)
    GRID = 5.0  # 격자 간격(km)
    SLAT1 = 30.0  # 투영 위도1(degree)
    SLAT2 = 60.0  # 투영 위도2(degree)
    OLON = 126.0  # 기준점 경도(degree)
    OLAT = 38.0  # 기준점 위도(degree)
    XO = 43  # 기준점 X좌표(GRID)
    YO = 136  # 기1준점 Y좌표(GRID)

    DEGRAD = math.pi / 180.0
    RADDEG = 180.0 / math.pi

    re = RE / GRID;
    slat1 = SLAT1 * DEGRAD
    slat2 = SLAT2 * DEGRAD
    olon = OLON * DEGRAD
    olat = OLAT * DEGRAD

    sn = math.tan(math.pi * 0.25 + slat2 * 0.5) / math.tan(math.pi * 0.25 + slat1 * 0.5)
    sn = math.log(math.cos(slat1) / math.cos(slat2)) / math.log(sn)
    sf = math.tan(math.pi * 0.25 + slat1 * 0.5)
    sf = math.pow(sf, sn) * math.cos(slat1) / sn
    ro = math.tan(math.pi * 0.25 + olat * 0.5)
    ro = re * sf / math.pow(ro, sn);
    rs = {};

    ra = math.tan(math.pi * 0.25 + (v1) * DEGRAD * 0.5)
    ra = re * sf / math.pow(ra, sn)

    theta = v2 * DEGRAD - olon
    if theta > math.pi:
        theta -= 2.0 * math.pi
    if theta < -math.pi:
        theta += 2.0 * math.pi
    theta *= sn
    rs['x'] = math.floor(ra * math.sin(theta) + XO + 0.5)
    rs['y'] = math.floor(ro - ra * math.cos(theta) + YO + 0.5)

    nx1 = str(rs['x'])
    ny1 = str(rs['y'])
    return nx1, ny1

    #  https://doriri.tistory.com/18
    #  https://oneshottenkill.tistory.com/557

        #https://velog.io/@yebinlee/Python-API-%EC%8B%A4%EC%8A%B5#-%EA%B7%B8%EB%9F%AC%EB%82%98--%F0%9F%A4%A8