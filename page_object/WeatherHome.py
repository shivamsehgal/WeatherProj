from selenium import webdriver
from selenium.common.exceptions import InvalidElementStateException
from selenium.webdriver.common.keys import Keys
from page_object.waits import DriverWaits
from selenium.webdriver.common.action_chains import ActionChains


class HomePage:

    advertisement_xpath = '//div[@class= "region-topAds regionTopAds DaybreakLargeScreen--regionTopAds--2bh4V"]'
    search_box_id = 'LocationSearch_input'
    feels_like_temp_xpath = '//span[@class="TodayDetailsCard--feelsLikeTempValue--2aogo"]'
    humidity_xpath = '//div[text()= "Humidity"]/following::span'
    pressure_xpath = '//div[text()= "Pressure"]/following::span'

    def __init__(self, driver):
        self.driver = driver
        driver.implicitly_wait(10)

    def wait_for_adv(self):
        wait = DriverWaits(self.driver)
        wait.wait_for_visibility(self.driver.find_element_by_xpath(self.advertisement_xpath), 15)

    def set_search_value(self, value):
        wait = DriverWaits(self.driver)
        wait.wait_for_visibility(self.driver.find_element_by_id(self.search_box_id), 10)
        search_box = self.driver.find_element_by_id(self.search_box_id)
        try:
            search_box.clear()
        except InvalidElementStateException:
            print('Unable to clear!!')

        search_box.send_keys(value)
        wait.hard_wait(1)
        search_box.send_keys(Keys.DOWN)
        wait.hard_wait(1)
        search_box.send_keys(Keys.RETURN)

    def get_temp_value(self):
        temp = self.driver.find_element_by_xpath(self.feels_like_temp_xpath)
        return temp.text

    def get_humidity_value(self):
        humidity = self.driver.find_element_by_xpath(self.humidity_xpath)
        return humidity.text

    def get_pressure_value(self):
        pressure = self.driver.find_element_by_xpath(self.pressure_xpath)
        return pressure.text
