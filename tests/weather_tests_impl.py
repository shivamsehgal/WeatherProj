import os
from selenium import webdriver
import requests
from selenium.webdriver.common.keys import Keys
from page_object.WeatherHome import HomePage


class ReusableMethods:

    def weather_web(self, driver, city_name: str):
        home = HomePage(driver)
        home.wait_for_adv()
        home.set_search_value(city_name)

        temp = home.get_temp_value()
        humidity = home.get_humidity_value()
        pressure = home.get_pressure_value()

        result = {
            'Temperature': float(temp[:len(temp)-1]),
            'Humidity': float(humidity[:len(humidity)-1]),
            'Pressure': float(pressure[:len(pressure)-3])
        }
        return result

    def weather_api(self, city_name):
        url = 'http://api.openweathermap.org/data/2.5/weather'
        params = (
            ('q', city_name),
            ('appid', 'fa2bd4187a376d5f28a203f77b9de956'),
            ('units', 'metric')
        )

        resp = requests.get(url, params=params)
        response = resp.json()
        temp = response['main']['temp']
        pressure = response['main']['pressure']
        humidity = response['main']['humidity']

        result = {
            'Temperature': float(temp),
            'Humidity': float(humidity),
            'Pressure': float(pressure)
        }
        return result


if __name__ == '__main__':
    test = ReusableMethods()
    test.weather_api('delhi')
    test.weather_web('delhi')
