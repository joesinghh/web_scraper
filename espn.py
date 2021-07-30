from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
import chromedriver_binary
from tkinter import *

def espn_data(driver):
    print("ESPN")

    try:
        main_card = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[5]/section/section/div/section[2]')))
        return main_card
    except Exception as e:
        print(e)


def get_main_card(main_card):
    print("espn")
    if main_card:
        try:

            card = main_card.find_elements_by_tag_name('h1')
        except Exception as e:
            print(e)
            card = None
        
    else:
        card = None
    return card
        

class News_espn(object):
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
        self.news   = Text(self.frame, bg='red',wrap=WORD,exportselection=False,height=count+1,relief='flat',justify='center')
        self.news.insert(END,text)
        self.news.place(relwidth=0.7,relheight=0.7,relx=0.15,rely=0.3)
        self.news.configure(state='disabled')


if __name__=='__main__':
    driver = webdriver.Chrome()
    driver.get("https://www.espn.in/football/")
    driver.implicitly_wait(4)
    main = espn_data(driver)
    get_main_card(main)

