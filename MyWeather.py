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
    # The Weather URL
    URL_CITY = f"https://www.metaweather.com/api/location/search/?query=Hong Kong"
    response_city = requests.request("GET", URL_CITY)
    city_title = json.loads(response_city.text)[0]["title"]
    city_id = json.loads(response_city.text)[0]["woeid"]
    URL_WEATHER = f"https://www.metaweather.com/api/location/{city_id}/"

    response_weather = requests.request("GET", URL_WEATHER)
    # Get the Json data to the weather_data
    weather_data = json.loads(response_weather.text)["consolidated_weather"]

    for index, day in enumerate(weather_data):
            # The Mini temperature
            min_temp.append(round(weather_data[index]["min_temp"],1))
            # The Max temperature
            max_temp.append(round(weather_data[index]["max_temp"],1))
            # The weather situation
            weather_state_name.append(weather_data[index]["weather_state_name"])
            # The weather situation short
            weather_state_abbr.append(weather_data[index]["weather_state_abbr"])
            # The Data
            applicable_date.append(weather_data[index]["applicable_date"])

    # Only get the 4 day data from the weather_data and return the 4 day data to the main script
    print("Got Weather Report")
    for i in range (0 , 4):
        print("Date : {0}, Min Temp : {1:.1f}, Max Temp : {2:.1f}"
              .format(weather_data[i]["applicable_date"], weather_data[i]["min_temp"], weather_data[i]["max_temp"]))
    
    return weather_data