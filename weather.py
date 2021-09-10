from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
import time
# from tkinter import *
options = webdriver.ChromeOptions()
options.add_argument("headless")

def search_by_location(driver):

    try : 
        temp = WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH,'/html/body/main/section[1]/div[2]/div/div[2]/div/div[2]/div/div/div/div/div/div/div/div/ul/li[1]/div/div/div/current-conditions-widget/div/div/div[2]/div[1]/div[1]')))
        desc = WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH,'/html/body/main/section[1]/div[2]/div/div[2]/div/div[2]/div/div/div/div/div/div/div/div/ul/li[1]/div/div/div/current-conditions-widget/div/div/div[2]/div[2]/div[2]')))
    except exceptions.TimeoutException:
        driver.refresh()
        temp = WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH,'/html/body/main/section[1]/div[2]/div/div[2]/div/div[2]/div/div/div/div/div/div/div/div/ul/li[1]/div/div/div/current-conditions-widget/div/div/div[2]/div[1]/div[1]')))
        desc = WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH,'/html/body/main/section[1]/div[2]/div/div[2]/div/div[2]/div/div/div/div/div/div/div/div/ul/li[1]/div/div/div/current-conditions-widget/div/div/div[2]/div[2]/div[2]')))

    
    return temp, desc

def weather_main():
    driver = webdriver.Chrome('chromedriver.exe',options=options)
    driver.get('https://www.weatherbug.com/')
    return driver

if __name__=='__main__':
    loc_driver = weather_main()
    loc_driver.get('https://www.weatherbug.com/')
    t, d = search_by_location(loc_driver)
    print(t.text,d.text)
    time.sleep(2)
    loc_driver.refresh()

