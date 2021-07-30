from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
import time
# from tkinter import *
optionschrome = webdriver.ChromeOptions()
optionschrome.add_argument("headless")

def search_by_location(driver):

    try : 
        temp = WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH,'/html/body/div/div[5]/div[1]/div[1]/a[1]/div[1]/div[1]/div/div/div[1]')))
        desc = WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH,'/html/body/div/div[5]/div[1]/div[1]/a[1]/div[2]/span[1]')))
    except exceptions.TimeoutException:
        driver.refresh()
        temp = WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH,'/html/body/div/div[5]/div[1]/div[1]/a[1]/div[1]/div[1]/div/div/div[1]')))
        desc = WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH,'/html/body/div/div[5]/div[1]/div[1]/a[1]/div[2]/span[1]')))

    
    return temp, desc

def weather_main():
    pass

if __name__=='__main__':
    loc_driver = weather_main("karnataka, bangalore")

    t, d = search_by_location(loc_driver)
    print(t.text,d.text)
    time.sleep(2)
    loc_driver.refresh()

