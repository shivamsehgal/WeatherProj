import os
import json
from selenium import webdriver
from tests.weather_tests_impl import ReusableMethods
from tests.matcher_exc import MatcherException


def variance_logic(app_value: float, api_value: float, variance):
    result = 0.0
    if app_value == api_value:
        result = 0.0
    try:
        result = (abs(app_value - api_value) / min(app_value, api_value)) * 100.0
    except ZeroDivisionError:
        result = max(app_value, api_value) * 100

    if result > float(variance):
        return MatcherException
    else:
        return 'success'


def comparator_logic(app_result: dict, api_result: dict):
    result_dict = {}
    print('Starting with commparator logic !!')
    print('Returning values APP/ API depending upon which has a greater value')
    # we will store platform from where greater values were received
    for city in app_result:
        inner_dict = {}
        if app_result[city]['Temperature'] > api_result[city]['Temperature']:
            inner_dict['Temperature'] = 'APP'
        else:
            inner_dict['Temperature'] = 'API'
        if app_result[city]['Humidity'] > api_result[city]['Humidity']:
            inner_dict['Humidity'] = 'APP'
        else:
            inner_dict['Humidity'] = 'API'
        if app_result[city]['Pressure'] > api_result[city]['Pressure']:
            inner_dict['Pressure'] = 'APP'
        else:
            inner_dict['Pressure'] = 'API'
        result_dict[city] = inner_dict

    print(result_dict)


def looping_logic(input_dict: json):
    path_to_chrome = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                  'exefiles', 'chromedriver.exe')
    url = 'https://weather.com/'

    # input_dict = {
    #    'City': ['Delhi', 'Chandigarh', 'Indore', 'Mumbai', 'Kolkata', 'New york', 'Texas'],
    #    'Variance': 3
    # }

    city_list = input_dict['City']
    result_dict_app = {}
    result_dict_api = {}

    inner_dict_app = {}
    inner_dict_api = {}

    driver = webdriver.Chrome(path_to_chrome)
    driver.maximize_window()
    driver.get(url)

    tests = ReusableMethods()

    for city in city_list:
        inner_dict_app = tests.weather_web(driver, city)
        inner_dict_api = tests.weather_api(city)

        result_dict_app[city] = inner_dict_app
        result_dict_api[city] = inner_dict_api

    print('Result received from Weather App : ')
    print(result_dict_app)
    print('Result received from Weather API : ')
    print(result_dict_api)

    comparator_logic(result_dict_app, result_dict_api)

    variance_dict = {}
    variance_value = input_dict['Variance']

    for city in result_dict_api:
        inner_dict = {'Temperature': variance_logic(result_dict_app[city]['Temperature'],
                                                    result_dict_api[city]['Temperature'], variance_value),
                      'Humidity': variance_logic(result_dict_app[city]['Humidity'],
                                                 result_dict_api[city]['Humidity'], variance_value),
                      'Pressure': variance_logic(result_dict_app[city]['Pressure'],
                                                 result_dict_api[city]['Pressure'], variance_value)}
        variance_dict[city] = inner_dict

    print('Printing variance matrix!!')
    print(variance_dict)


if __name__ == '__main__':
    input_dict = {
        'City': ['Delhi', 'Chandigarh', 'Indore', 'Mumbai', 'Kolkata', 'New york', 'Texas'],
        'Variance': 3
    }
    json_str = json.dumps(input_dict)
    json_input = json.loads(json_str)
    looping_logic(json_input)
