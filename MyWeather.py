#!/usr/bin/env python
# coding: utf-8

import json
import requests

def GetWeatherReport():
    min_temp = []
    max_temp = []
    weather_state_name = []
    weather_state_abbr = []
    applicable_date = []
    URL_CITY = f"https://www.metaweather.com/api/location/search/?query=Hong Kong"
    response_city = requests.request("GET", URL_CITY)
    city_title = json.loads(response_city.text)[0]["title"]
    city_id = json.loads(response_city.text)[0]["woeid"]
    URL_WEATHER = f"https://www.metaweather.com/api/location/{city_id}/"

    response_weather = requests.request("GET", URL_WEATHER)
    weather_data = json.loads(response_weather.text)["consolidated_weather"]

    for index, day in enumerate(weather_data):
            # 最低溫度
            min_temp.append(round(weather_data[index]["min_temp"],1))
            # 最高溫度
            max_temp.append(round(weather_data[index]["max_temp"],1))
            # 天氣情况
            weather_state_name.append(weather_data[index]["weather_state_name"])
            # 天氣情况縮寫
            weather_state_abbr.append(weather_data[index]["weather_state_abbr"])
            # 日期
            applicable_date.append(weather_data[index]["applicable_date"])

    print("Got Weather Report")
    for i in range (0 , 4):
        print("Date : {0}, Min Temp : {1:.1f}, Max Temp : {2:.1f}"
              .format(weather_data[i]["applicable_date"], weather_data[i]["min_temp"], weather_data[i]["max_temp"]))
    
    return weather_data