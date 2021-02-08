import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class DriverWaits:

    def __init__(self, driver):
        self.driver = driver

    def wait_for_visibility(self, element, time):
        try:
            WebDriverWait(self.driver, time).until(
                EC.visibility_of(element)
            )
        except:
            print('Element not visible!!')

    def hard_wait(self, wait_time):
        time.sleep(wait_time)