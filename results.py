from selenium import webdriver
from selenium import common
import selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
from tkinter import *

optionschrome = webdriver.ChromeOptions()
optionschrome.add_argument("headless")

def get_score_block(driver,sport='football'):
    
    if sport.lower()!='boxing':
        try:

            section = WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.CLASS_NAME ,"event")))
        except exceptions.TimeoutException:
            driver.refresh()
            section = WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.CLASS_NAME ,"event")))

    else:
        try:
            section = WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.ID ,"main")))
        except exceptions.TimeoutException:
            driver.refresh()
            section = WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.ID ,"main")))


    return section
    

def get_results(section,sport,driver):
    try:
        if sport.lower()=='football':
            home = section.find_elements_by_class_name('event__participant.event__participant--home')
            away = section.find_elements_by_class_name('event__participant.event__participant--away')
            result  = section.find_elements_by_class_name('event__scores')
            return home, away, result

        elif sport.lower()=='cricket':
            # finished = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[5]/div[1]/div/div[1]/div[2]/div[5]/div/div[1]/div[1]/div[4]/div')))
            # finished.click()
            home  = section.find_elements_by_class_name('event__participant.event__participant--home')
            home_score = section.find_elements_by_class_name('event__score.event__score--home')
            away  = section.find_elements_by_class_name('event__participant.event__participant--away')
            away_score = section.find_elements_by_class_name('event__score.event__score--away')
            print("cricket",len(home))

            return home, home_score, away, away_score

        elif sport.lower()=='basketball' or sport.lower()=='rugby':
            home  = section.find_elements_by_class_name('event__participant.event__participant--home')
            home_score = section.find_elements_by_class_name('event__score.event__score--home')
            away  = section.find_elements_by_class_name('event__participant.event__participant--away')
            away_score = section.find_elements_by_class_name('event__score.event__score--away')
            return home, home_score, away, away_score

        elif sport.lower()=='boxing':
            date = section.find_elements_by_tag_name('li')
            result  = section.find_elements_by_tag_name('a')
            return date, result

        elif sport.lower()=='golf':
            rank = section.find_elements_by_class_name('event__rating.rank')
            name = section.find_elements_by_class_name('event__participantName')
            par = section.find_elements_by_class_name('event__center.event__result--par')
            today = section.find_elements_by_class_name('event__center.event__result--today')
            result = section.find_elements_by_class_name('event__center.event__result--roundAll.event__result')
            country = section.find_elements_by_class_name('flag')
            print("Golf",len(name))
            return rank, name, par, today, result, country


    except Exception as e:
        print(e)
    return None, None, None

def get_football():
    football_driver = webdriver.Chrome('chromedriver.exe',options=optionschrome)
    football_driver.get("https://www.flashscore.co.uk")
    section = get_score_block(football_driver,'football')
    return football_driver, section

def get_cricket():
    cricket_driver = webdriver.Chrome('chromedriver.exe')
    cricket_driver.get("https://www.flashscore.co.uk/cricket/")
    section = get_score_block(cricket_driver,'cricket')
    return cricket_driver, section

def get_basketball():
    basketball_driver = webdriver.Chrome('chromedriver.exe',options=optionschrome)
    basketball_driver.get("https://www.flashscore.co.uk/basketball/")
    section = get_score_block(basketball_driver,'basketball')
    return basketball_driver, section

def get_rugby():
    rugby_driver = webdriver.Chrome('chromedriver.exe',options=optionschrome)
    rugby_driver.get("https://www.flashscore.co.uk/rugby-union/")
    section = get_score_block(rugby_driver,'rugby')
    return rugby_driver, section

def get_golf():
    golf_driver = webdriver.Chrome('chromedriver.exe')
    golf_driver.get("https://www.flashscore.co.uk/golf/")
    section = get_score_block(golf_driver,'golf')
    return golf_driver, section

def get_boxing():
    boxing_driver = webdriver.Chrome('chromedriver.exe',options=optionschrome)
    boxing_driver.get("https://www.boxing247.com/boxing-results")
    section = get_score_block(boxing_driver,'boxing')
    return boxing_driver, section


class Football(object):
    def __init__(self, frame, home, away, result):
        self.homedata = home
        self.awaydata = away
        self.resultdata = result
        self.frame = frame
    
    def create_widgets(self):
        
        self.home   = Text(self.frame,wrap=WORD,exportselection=False,relief='flat')
        self.home.insert(END,self.homedata)
        self.home.place(relwidth=0.22,height=40,relx=0.2,y=300)

        self.result = Text(self.frame,wrap=WORD,exportselection=False,relief='flat')
        self.result.insert(END, self.resultdata)
        self.result.place(height=40,relx=0.43,y=300,relwidth=0.14)

        self.away = Text(self.frame,wrap=WORD,exportselection=False,relief='flat')
        self.away.insert(END, self.awaydata)
        self.away.place(relwidth=0.22,height=40,relx=0.58,y=300)

class BasketballRugby(object):

    def __init__(self, frame, home, home_score, away, away_score):
        self.frame = frame
        self.home_score = home_score
        self.home = home
        self.away_score = away_score
        self.away = away

    def create_widgets(self):
        self.homew   = Text(self.frame,wrap=WORD,exportselection=False,relief='flat')
        self.homew.insert(END,self.home)
        self.homew.place(relwidth=0.22,height=40,relx=0.2,y=300)

        self.result = Text(self.frame,wrap=WORD,exportselection=False,relief='flat')
        self.result.insert(END, self.home_score+" - "+self.away_score)
        self.result.place(height=40,relx=0.43,y=300,relwidth=0.14)

        self.awayw = Text(self.frame,wrap=WORD,exportselection=False,relief='flat')
        self.awayw.insert(END, self.away)
        self.awayw.place(relwidth=0.22,height=40,relx=0.58,y=300)

class Cricket(object):

    def __init__(self, frame, home, home_score, away, away_score):
        self.frame = frame
        self.home_score = home_score
        self.home = home
        self.away_score = away_score
        self.away = away

    def create_widgets(self):
        print("hello cricket")
        self.homew   = Text(self.frame,wrap=WORD,exportselection=False,)
        self.homew.insert(END,self.home)
        self.homew.place(relwidth=0.22,height=40,relx=0.2,y=300)

        self.result = Text(self.frame,wrap=WORD,exportselection=False,)
        self.result.insert(END, self.home_score+" - "+self.away_score)
        self.result.place(height=40,relx=0.43,y=300,relwidth=0.14)

        self.awayw = Text(self.frame,wrap=WORD,exportselection=False,)
        self.awayw.insert(END, self.away)
        self.awayw.place(relwidth=0.22,height=40,relx=0.58,y=300)
    

class Boxing(object):

    def __init__(self, frame, date, result):
        self.frame = frame
        self.datevalue = date
        self.news = result 


    def create_widgets(self):
        self.newsw = Text(self.frame,wrap=WORD,exportselection=False,)
        self.newsw.insert(END, self.news)
        self.newsw.place(height=100,relx=0.2,relwidth=0.6, y=300)

class Golf(object):
    
    def __init__(self,frame, rank, name, par, today, result, country):
        self.frame = frame
        self.rank = rank
        self.name = name
        self.par = par
        self.today = today
        self.result = result
        self.country = country
    
    def create_widgets(self):
        print("hello golf")
        self.rankw = Text(self.frame, wrap=WORD,exportselection=False)
        self.rankw.insert(END, self.rank)
        self.rankw.place(width=70,height=40,x=350,y=300)


if __name__=='__main__':
    driver  = webdriver.Chrome('chromedriver.exe')
    driver.get('https://www.flashscore.co.uk/cricket/')
    section = get_score_block(driver,'cricket')
    # print(section)
    home, home_score, away, away_score = get_results(section,'cricket',driver)
    # home, home_score = get_results(section,'basketball',driver)
    
    # print(len(home),len(result)
    # print(home)
    # print(away)
    # print(result)
    for i in range(len(home)):
        if "/" in home_score[i].text or  "/" in away_score[i].text:
            print(home[i].text,home_score[i].text)
    # rank, name, par, today, result, country = get_results(section,'golf',driver)
    # print(len(rank),print(len(par)))
    # print(today,result)
    # print(len(country))
    # for i in range(len(rank)):
    #         print(country[i].get_attribute('title'))
    
    driver.quit()



"""

golf
event__rating rank
event__participantName
event__center event__result--par fontBold
event__center event__result--today undefined
event__center event__result--roundAll event__result--grey
/html/body/div[6]/div[1]/div/div[1]/div[2]/div[5]/div/section/div/div/div[11]/div[3]
/html/body/div[6]/div[1]/div/div[1]/div[2]/div[5]/div/section/div/div/div[2]/div[3]

/html/body/div[6]/div[1]/div/div[1]/div[2]/div[5]/div/section/div/div/div[25]/div[3]
title : /html/body/div[6]/div[1]/div/div[1]/div[2]/div[5]/div/section/div/div/div[10]/div[1]/div

class event__match event__match--oneLine 
event__title--type
event__title--name
event__titleBox
event__participant event__participant--home
event__participant event__participant--away
event__scores 

cricket
extraInfo__text extraInfo__sentence - judgement
event__score event__score--away
event__score event__score--home
event__participant event__participant--home
event__participant event__participant--away fontBold
tabs__text tabs__text--default

basketball
event__participant event__participant--home fontBold
event__participant event__participant--away
event__score event__score--home
event__score event__score--away

ruby
https://www.flashscore.co.uk/rugby-union/
event__participant event__participant--home fontBold
event__participant event__participant--away
event__score event__score--home
event__score event__score--away


boxing
lcp_instance_0
https://www.boxing247.com/boxing-results


"""