from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
from tkinter import *

options = webdriver.ChromeOptions()
options.add_argument("headless")

def bbc_data(driver):  
   
    

    try :                                                                
        main_card = WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[8]/div[3]/div/div[2]/div[1]/div/div[1]/div[1]')))

        second_card = WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[8]/div[3]/div/div[2]/div[1]/div/div[1]/div[2]')))
    except Exception as e:
        print("CARD NOT FOUND",e)
        main_card = None
        second_card = None
    return main_card, second_card



def get_main_card(main_card):
    if main_card:
        try:
            
            card = main_card.find_elements_by_tag_name('h3')

        except:
            print("DATA not FOUND")
            card = None
            
        
    else:
        card = None
    return card
        

class News_bbc(object):
    def __init__(self, frame, news_data, y, master):
        self.frame = frame
        self.news_data = news_data
        self.y_value = y
        self.master = master

    def create_news(self):
        text = self.news_data
        count = text.count("\n")
        text = text.replace("\n"," ")
        print(text)
        
        self.news   = Text(self.frame, bg='white',wrap=WORD,exportselection=False,height=count+1,relief='flat')
        self.news.insert(END,text)
        self.news.place(relwidth=0.7,relheight=0.6,relx=0.15,rely=0.3)
        self.news.configure(state='disabled')

def main(path,dr):
    dr.get(path)
    dr.implicitly_wait(4)
    main_card, second_card = bbc_data(dr)
    return get_main_card(main_card), get_main_card(second_card)

def bbc_sport_driver():
    driver  = webdriver.Chrome('chromedriver.exe',options=options)
    return driver

if __name__=='__main__':
    driver = webdriver.Chrome()
    driver.get("https://www.bbc.com/sport/football")
    driver.implicitly_wait(4)
    main_card, second_card = bbc_data(driver)
    get_main_card(second_card)
    get_main_card(main_card)

