from enum import unique
import selenium
from data import twitter_data, twitter_login, extract_data, scroll_down_page, generate_tweet_id
from tkinter import *
from tkinter import ttk
from tweets import TwitterCards
from threading import Thread
from PIL import Image, ImageTk
from tkinter import messagebox
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from collections.abc import Iterable
from bbc_sports import bbc_data, get_main_card, News_bbc, main, bbc_sport_driver
from espn import espn_data, get_main_card, News_espn
import random
import time
from tkinter import ttk
import platform
import sys
from results import get_score_block, get_results, Football, BasketballRugby, Boxing, Golf, Cricket, get_football, get_cricket,\
get_rugby, get_basketball, get_golf, get_boxing
import requests
from datetime import datetime
from weather import search_by_location, weather_main
from search import search_sport




optionschrome = webdriver.ChromeOptions()
optionschrome.add_argument("headless")
# optionschrome = None

twitter_driver = webdriver.Chrome('chromedriver.exe',options=optionschrome)
twitter_driver.get("https://twitter.com/login")


until_exit = 0
city = None
region = None
y_twitter = 40
y_bbc = y_twitter+190
y_espn = y_bbc+190

search_1 = 0
search_2 = 0
search_3 = 0


class ScrollFrame(Frame):
    def __init__(self, parent):
        super().__init__(parent) # create a frame (self)

        self.canvas = Canvas(self, borderwidth=0, background="#ffffff")          #place canvas on self
        self.viewPort = Frame(self.canvas, background="#ffffff")                    #place a frame on the canvas, this frame will hold the child widgets 
        self.vsb = Scrollbar(self, orient="vertical", command=self.canvas.yview) #place a scrollbar on self 
        self.canvas.configure(yscrollcommand=self.vsb.set)                          #attach scrollbar action to scroll of canvas

        self.vsb.pack(side="right", fill="y")                                       #pack scrollbar to right of self
        self.canvas.pack(side="left", fill="both", expand=True)                     #pack canvas to left of self and expand to fil
        self.canvas_window = self.canvas.create_window((4,4), window=self.viewPort, anchor="nw",            #add view port frame to canvas
                                  tags="self.viewPort")

        self.viewPort.bind("<Configure>", self.onFrameConfigure)                       #bind an event whenever the size of the viewPort frame changes.
        self.canvas.bind("<Configure>", self.onCanvasConfigure)                       #bind an event whenever the size of the canvas frame changes.
            
        self.viewPort.bind('<Enter>', self.onEnter)                                 # bind wheel events when the cursor enters the control
        self.viewPort.bind('<Leave>', self.onLeave)                                 # unbind wheel events when the cursorl leaves the control

        self.onFrameConfigure(None)                                                 #perform an initial stretch on render, otherwise the scroll region has a tiny border until the first resize

    def onFrameConfigure(self, event):                                              
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))                 #whenever the size of the frame changes, alter the scroll region respectively.

    def onCanvasConfigure(self, event):
        '''Reset the canvas window to encompass inner frame when required'''
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width = canvas_width)            #whenever the size of the canvas changes alter the window region respectively.

    def onMouseWheel(self, event):                                                  # cross platform scroll wheel event
        if platform.system() == 'Windows':
            # self.canvas.yview_scroll(int(-1* (event.delta/120)), "units")
            pass
        elif platform.system() == 'Darwin':
            self.canvas.yview_scroll(int(-1 * event.delta), "units")
        else:
            if event.num == 4:
                self.canvas.yview_scroll( -1, "units" )
            elif event.num == 5:
                self.canvas.yview_scroll( 1, "units" )
    
    def onEnter(self, event):                                                       # bind wheel events when the cursor enters the control
        if platform.system() == 'Linux':
            self.canvas.bind_all("<Button-4>", self.onMouseWheel)
            self.canvas.bind_all("<Button-5>", self.onMouseWheel)
        else:
            self.canvas.bind_all("<MouseWheel>", self.onMouseWheel)

    def onLeave(self, event):                                                       # unbind wheel events when the cursorl leaves the control
        if platform.system() == 'Linux':
            self.canvas.unbind_all("<Button-4>")
            self.canvas.unbind_all("<Button-5>")
        else:
            self.canvas.unbind_all("<MouseWheel>")

def options_raise():
    def thread_options():

        options_frame.tkraise()
        root.wm_title("Twitter | Options")
        twitter_login(twitter_driver,username.get(),password.get())
    
    t = Thread(target=thread_options)
    t.start()

def display_data():
    messagebox.showinfo("Please wait","""WebScraping is an slow process, loading results may take time.\n
    Beep. Boop. Beep.""")

    baseframe.tkraise()
    root.wm_title("News")

    t = Thread(target=twitter_feed,args=())
    t.start()
    t1 = Thread(target=bbc_news_sports, args=())
    t1.start()
    t2 = Thread(target=espn_news,args=())
    t2.start()

    t3 = Thread(target=match_results,args=())
    t3.start()

    
def twitter_feed():
    unique_tweets = set()
    last_position = None
    end_of_scroll_region = False

    while  not end_of_scroll_region:
        cards = twitter_data(twitter_driver)
        for card in cards:
            try:
                tweet = extract_data(card)
                if not tweet:
                    continue
                else:
                    tweet_id = generate_tweet_id(tweet)
                    if tweet_id not in unique_tweets and isinstance(tweet,Iterable):

                        unique_tweets.add(tweet_id)
                        t = TwitterCards(twitter_frame, tweet, y_twitter,root)
                        thread_tweet = Thread(target=t.create_card,)
                        thread_tweet.start()
                        time.sleep(10)
                        t.user.destroy()
                        t.tweet_text.destroy()
                        

            except exceptions.StaleElementReferenceException as e:
                print("Error",e)
                continue
            

        last_position, end_of_scroll_region = scroll_down_page(twitter_driver, last_position)

def bbc_news_sports():
    dr = bbc_sport_driver()
    sports = ['football','olympics','cricket','golf','rugby-union','tennis','boxing']
    i = 0
    while not until_exit and i<len(sports):

        path = "https://www.bbc.com/sport/{}".format(sports[i])
        first_data, second_data  = main(path,dr)
        
        dataset  = first_data+second_data

        random.shuffle(dataset)
        for data in dataset:
            if data:
                try:
                    data = data.text
                    b = News_bbc(bbc_frame, data, y_bbc, root)
                    b.create_news()
                    if until_exit:
                        dr.quit()
                        break
                    time.sleep(10)
                    b.news.destroy()
                except Exception as e:
                    print(e)
        i+=1
        if i==len(sports):
            i = 0

def espn_news():
    driver = webdriver.Chrome('chromedriver.exe',options=optionschrome)
    sports = ['boxing','football','golf','olympics','rugby','cricket']
    i = 0
    while not until_exit and i<len(sports):
        
        driver.get("https://www.espn.co.uk/{0}/".format(sports[i]))
        first_card = espn_data(driver)
        first_data  = get_main_card(first_card)
        
        dataset  = first_data
        random.shuffle(dataset)
        for data in dataset:
            if data and len(data.text.split(" "))>4:
                try:
                    data = data.text

                    b = News_bbc(espn_frame, data, y_espn, root)
                    b.create_news()
                    if until_exit:
                        driver.quit()
                        break
                    time.sleep(10)
                    b.news.destroy()
                except Exception as e:
                    print(e)
        i+=1
        
        if i==len(sports):
            i=0
        
        
def match_results():
    if option1var.get()!="None":
        t4 = Thread(target=first_results,args=(option1var.get(),))
        t4.start()
    
    if option2var.get()!="None":
        t5 = Thread(target=second_results, args=(option2var.get(),))
        t5.start()
    if option3var.get()!="None":
        t6 = Thread(target=third_results,args=(option3var.get(),))
        t6.start()

def first_results(v):
    value = v.lower()

    if value=='basketball' or value=='rugby':
        path = 'https://www.flashscore.co.uk/{}/'.format(value)
        frame1_driver, block = get_basketball()
        if value=='rugby':
            frame1_driver, block = get_rugby()
            path = 'https://www.flashscore.co.uk/rugby-union/'

    elif value=='football':
        frame1_driver, block = get_football()
        path = 'https://www.flashscore.co.uk'
    elif value=='cricket':
        frame1_driver, block = get_cricket()
        path = 'https://www.flashscore.co.uk/{}/'.format(value)
    elif value=='golf':
        frame1_driver, block = get_golf()
        path  = 'https://www.flashscore.co.uk/{}/'.format(value)
    elif value=='boxing':
        frame1_driver, block = get_boxing()
        path = 'https://www.boxing247.com/boxing-results'
        

    Label(frame1,text=value.upper(),bg='white',font=("Arial",16)).place(relx=0.4,relwidth=0.2,y=2)
    Label(frame1,text=path,bg='white',font=("Arial",12)).place(relx=0.3,y=80)
    searchs1.config(state='normal')
    search_button_1.config(state='normal')
    reset_button1.config(state='normal')
    
    if block:
        if value=='football':
            home, away, result = get_results(block, value, frame1_driver)
            i = 0
            while i<len(home) and not search_1:
                r = result[i].text.replace("\n"," ")
                if r!="-" and r!=" - ":
                    sresult = Football(frame1, home[i].text, away[i].text, r)
                    sresult.create_widgets()
                    if search_1:
                        frame1_driver.quit()
                        return
                    time.sleep(10)
                    sresult.home.destroy()
                    sresult.away.destroy()
                    sresult.result.destroy()
                    i+=1
                if i==len(home):
                    i = 0

        elif value=='cricket':
            home, homescore, away, awayscore  = get_results(block, value, frame1_driver)
            i = 0
            while i<len(home) and not search_1:
                sresult = Cricket(frame1, home[i].text, homescore[i].text, away[i].text, awayscore[i].text)
                sresult.create_widgets()
                if search_1:
                    frame1_driver.quit()
                    return
                time.sleep(10)
                sresult.homew.destroy()
                sresult.awayw.destroy()
                sresult.result.destroy()
                i+=1
                if i==len(home):
                    i = 0
                    
            
        elif value=='rugby' or value=='basketball':
            home, homescore, away, awayscore  = get_results(block, value, frame1_driver)
            i = 0
            while i<len(home) and not search_1:
                if "-" not in homescore[i].text:
                    sresult = BasketballRugby(frame1, home[i].text, homescore[i].text, away[i].text, awayscore[i].text)
                    sresult.create_widgets()
                    if search_1:
                        frame1_driver.quit()
                        return
                    time.sleep(10)
                    sresult.homew.destroy()
                    sresult.awayw.destroy()
                    sresult.result.destroy()
                    i+=1
                if i==len(home):
                    i = 0

        elif value=='boxing':
            searchs1.config(state='disabled')
            search_button_1.config(state='disabled')
            reset_button1.config(state='disabled')
            date, result  = get_results(block, value, frame1_driver)
            i = 0
            while i<len(date) and not search_1:
                sresult = Boxing(frame1, date[i].text, result[i].text,)
                sresult.create_widgets()
                if search_1:
                    frame1_driver.quit()
                    return
                time.sleep(10)
                sresult.newsw.destroy()

                i+=1
                if i==len(date):
                    i = 0
        elif value=='golf':
            Label(frame1,text="Player",justify='left',bg='white').place(relx=0.2,relwidth=0.2,height=70,y=260)
            Label(frame1,text="par",justify='left',bg='white').place(relx=0.42,relwidth=0.1,height=70,y=260)
            Label(frame1,text="T",justify='left',bg='white').place(relx=0.54,relwidth=0.1,height=70,y=260)
            Label(frame1,text="R",justify='left',bg='white').place(relx=0.66,relwidth=0.1,height=70,y=260)
            rank, name, par, today, result, country  = get_results(block, value, frame1_driver)
            i = 0
            while i<len(rank) and not search_1:
                if name[i].text.lower()!='player':

                    sresult = Golf(frame1,rank[i].text, name[i].text, par[i].text, today[i].text, result[i].text, country[i].text )
                    sresult.create_widgets()
                    if search_1:
                        frame1_driver.quit()
                        return
                    time.sleep(10)
                    sresult.rankw.destroy()
                    sresult.countryw.destroy()
                    sresult.namew.destroy()
                    sresult.parw.destroy()
                i+=1
                if i==len(rank):
                    i = 0

def second_results(v):
    value = v.lower()

    if value=='basketball' or value=='rugby':
        path = 'https://www.flashscore.co.uk/{}/'.format(value)
        frame2_driver, block = get_basketball()
        if value=='rugby':
            frame2_driver, block = get_rugby()
            path = 'https://www.flashscore.co.uk/rugby-union/'

    elif value=='football':
        frame2_driver, block = get_football()
        path = 'https://www.flashscore.co.uk'
    elif value=='cricket':
        frame2_driver, block = get_cricket()
        path = 'https://www.flashscore.co.uk/{}/'.format(value)
    elif value=='golf':
        frame2_driver, block = get_golf()
        path  = 'https://www.flashscore.co.uk/{}/'.format(value)
    elif value=='boxing':
        frame2_driver, block = get_boxing()
        path = 'https://www.boxing247.com/boxing-results'
        
  
    Label(frame2,text=value.upper(),bg='white',font=("Arial",16)).place(relx=0.4,relwidth=0.2,y=2)
    Label(frame2,text=path,bg='white',font=("Arial",12)).place(relx=0.3,y=80)
    searchs2.config(state='normal')
    search_button_2.config(state='normal')
    reset_button2.config(state='normal')
    
    if block:
        if value=='football':
            home, away, result = get_results(block, value, frame2_driver)
            i = 0
            while i<len(home) and not search_2:
                r = result[i].text.replace("\n"," ")
                if r!="-" and r!=" - ":
                    sresult = Football(frame2, home[i].text, away[i].text, r)
                    sresult.create_widgets()
                    if search_2:
                        frame2_driver.quit()
                        return
                    time.sleep(10)
                    sresult.home.destroy()
                    sresult.away.destroy()
                    sresult.result.destroy()
                    i+=1
                if i==len(home):
                    i = 0

        elif value=='cricket':
            home, homescore, away, awayscore  = get_results(block, value, frame2_driver)
            i = 0
            while i<len(home) and not search_2:
                sresult = Cricket(frame2, home[i].text, homescore[i].text, away[i].text, awayscore[i].text)
                sresult.create_widgets()
                if search_2:
                    frame2_driver.quit()
                    return
                time.sleep(10)
                sresult.homew.destroy()
                sresult.awayw.destroy()
                sresult.result.destroy()
                i+=1
                if i==len(home):
                    i = 0
                    
            
        elif value=='rugby' or value=='basketball':
            home, homescore, away, awayscore  = get_results(block, value, frame2_driver)

            i = 0
            while i<len(home) and not search_2:
                if "-" not in homescore[i].text:
                    sresult = BasketballRugby(frame2, home[i].text, homescore[i].text, away[i].text, awayscore[i].text)
                    sresult.create_widgets()
                    if search_2:
                        frame2_driver.quit()
                        return
                    time.sleep(10)
                    sresult.homew.destroy()
                    sresult.awayw.destroy()
                    sresult.result.destroy()
                    i+=1
                if i==len(home):
                    i = 0

        elif value=='boxing':
            searchs2.config(state='disabled')
            search_button_2.config(state='disabled')
            reset_button2.config(state='disabled')
            date, result  = get_results(block, value, frame2_driver)
            i = 0
            while i<len(date) and not search_2:
                sresult = Boxing(frame2, date[i].text, result[i].text,)
                sresult.create_widgets()
                if search_2:
                    frame2_driver.quit()
                    return
                time.sleep(10)
                sresult.newsw.destroy()

                i+=1
                if i==len(date):
                    i = 0
        elif value=='golf':
            Label(frame2,text="Player",justify='left',bg='white').place(relx=0.2,relwidth=0.2,height=70,y=260)
            Label(frame2,text="par",justify='left',bg='white').place(relx=0.42,relwidth=0.1,height=70,y=260)
            Label(frame2,text="T",justify='left',bg='white').place(relx=0.54,relwidth=0.1,height=70,y=260)
            Label(frame2,text="R",justify='left',bg='white').place(relx=0.66,relwidth=0.1,height=70,y=260)
            rank, name, par, today, result, country  = get_results(block, value, frame2_driver)
            i = 0
            while i<len(rank) and not search_2:
                sresult = Golf(frame2,rank[i].text, name[i].text, par[i].text, today[i].text, result[i].text, country[i].text )
                sresult.create_widgets()
                if search_2:
                    frame2_driver.quit()
                    return
                time.sleep(10)
                sresult.rankw.destroy()
                sresult.countryw.destroy()
                sresult.namew.destroy()
                sresult.parw.destroy()
                i+=1
                if i==len(rank):
                    i = 0

def third_results(v):
    value = v.lower()
    if value=='basketball' or value=='rugby':
        path = 'https://www.flashscore.co.uk/{}/'.format(value)
        frame3_driver, block = get_basketball()
        if value=='rugby':
            frame3_driver, block = get_rugby()
            path = 'https://www.flashscore.co.uk/rugby-union/'

    elif value=='football':
        frame3_driver, block = get_football()
        path = 'https://www.flashscore.co.uk'
    elif value=='cricket':
        frame3_driver, block = get_cricket()
        path = 'https://www.flashscore.co.uk/{}/'.format(value)
    elif value=='golf':
        frame3_driver, block = get_golf()
        path  = 'https://www.flashscore.co.uk/{}/'.format(value)
    elif value=='boxing':
        frame3_driver, block = get_boxing()
        path = 'https://www.boxing247.com/boxing-results'
        

    Label(frame3,text=value.upper(),bg='white',font=("Arial",16)).place(relx=0.4,relwidth=0.2,y=2)
    Label(frame3,text=path,bg='white',font=("Arial",12)).place(relx=0.3,y=80)
    searchs3.config(state='normal')
    search_button_3.config(state='normal')
    reset_button3.config(state='normal')
    
    if block:
        if value=='football':
            home, away, result = get_results(block, value, frame3_driver)
            i = 0
            while i<len(home) and not search_3:
                r = result[i].text.replace("\n"," ")
                if r!="-" and r!=" - ":
                    sresult = Football(frame3, home[i].text, away[i].text, r)
                    sresult.create_widgets()
                    if search_3:
                        frame3_driver.quit()
                        return
                    time.sleep(10)
                    sresult.home.destroy()
                    sresult.away.destroy()
                    sresult.result.destroy()
                    i+=1
                if i==len(home):
                    i = 0

        elif value=='cricket':
            home, homescore, away, awayscore  = get_results(block, value, frame3_driver)
            i = 0
            while i<len(home) and not search_3:
                if "/" in homescore[i].text or "/" in awayscore[i].text:
                    sresult = Cricket(frame3, home[i].text, homescore[i].text, away[i].text, awayscore[i].text)
                    sresult.create_widgets()
                    if search_3:
                        frame3_driver.quit()
                        return
                    time.sleep(10)
                    sresult.homew.destroy()
                    sresult.awayw.destroy()
                    sresult.result.destroy()
                    i+=1
                if i==len(home):
                    i = 0
                    
            
        elif value=='rugby' or value=='basketball':
            home, homescore, away, awayscore  = get_results(block, value, frame3_driver)
            
            i = 0
            while i<len(home) and not search_3:
                if "-" not in homescore[i].text:
                    sresult = BasketballRugby(frame3, home[i].text, homescore[i].text, away[i].text, awayscore[i].text)
                    sresult.create_widgets()
                    if search_3:
                        frame3_driver.quit()
                        return
                    time.sleep(10)
                    sresult.homew.destroy()
                    sresult.awayw.destroy()
                    sresult.result.destroy()
                    i+=1
                if i==len(home):
                    i = 0

        elif value=='boxing':
            searchs3.config(state='disabled')
            search_button_3.config(state='disabled')
            reset_button3.config(state='disabled')
            date, result  = get_results(block, value, frame3_driver)
            i = 0
            while i<len(date) and not search_3:
                sresult = Boxing(frame3, date[i].text, result[i].text,)
                sresult.create_widgets()
                if search_3:
                    frame3_driver.quit()
                    return
                time.sleep(10)
                sresult.newsw.destroy()

                i+=1
                if i==len(date):
                    i = 0

        elif value=='golf':
            Label(frame3,text="Player",justify='left',bg='white').place(relx=0.2,relwidth=0.2,height=70,y=260)
            Label(frame3,text="par",justify='left',bg='white').place(relx=0.42,relwidth=0.1,height=70,y=260)
            Label(frame3,text="T",justify='left',bg='white').place(relx=0.54,relwidth=0.1,height=70,y=260)
            Label(frame3,text="R",justify='left',bg='white').place(relx=0.66,relwidth=0.1,height=70,y=260)
            rank, name, par, today, result, country  = get_results(block, value, frame3_driver)

            i = 0
            while i<len(rank) and not search_3:

                sresult = Golf(frame3,rank[i].text, name[i].text, par[i].text, today[i].text, result[i].text, country[i].text )
                sresult.create_widgets()
                if search_3:
                    frame3_driver.quit()
                    return
                time.sleep(10)
                sresult.rankw.destroy()
                i+=1
                if i==len(rank):
                    i = 0

def search_frame1():
    value = option1var.get().lower()
    global search_1
    search_1 = 1
    query = league1.get()
    query = query.replace(" ","")
    
    if value == 'football':
        local_driver, section = search_sport('football',query.lower())
        if local_driver==None:
            return
        home, away, result = get_results(section, value, local_driver)
        i = 0
        while i<len(home) and search_1:
            r = result[i].text.replace("\n"," ")
            if r!="-" and r!=" - ":
                sresult = Football(frame1, home[i].text, away[i].text, r)
                sresult.create_widgets()
                if not search_1:
                    local_driver.quit()
                    return
                time.sleep(10)
                sresult.home.destroy()
                sresult.away.destroy()
                sresult.result.destroy()
                i+=1
            if i==len(home):
                i = 0

    elif value == 'basketball' or value == 'rugby':
        if value=='basketball':
            local_driver, section = search_sport('basketball',query.lower())
        else :
            local_driver, section = search_sport('rugby',query.lower())
        if local_driver==None:
            return
        home, homescore, away, awayscore  = get_results(section, value, local_driver)
            
        i = 0
        while i<len(home) and search_1:
            if "-" not in homescore[i].text:
                sresult = BasketballRugby(frame1, home[i].text, homescore[i].text, away[i].text, awayscore[i].text)
                sresult.create_widgets()
                if not search_sport:
                    local_driver.quit()
                    return

                time.sleep(10)
                sresult.homew.destroy()
                sresult.awayw.destroy()
                sresult.result.destroy()
                i+=1
            if i==len(home):
                i = 0

    elif value == 'cricket' :
        local_driver, section = search_sport('cricket',query.lower())
        if local_driver==None:
            return
        home, homescore, away, awayscore  = get_results(section, value, local_driver)
        i = 0
        while i<len(home) and search_1:
            sresult = Cricket(frame1, home[i].text, homescore[i].text, away[i].text, awayscore[i].text)
            sresult.create_widgets()
            if not search_1:
                local_driver.quit()
                return
            time.sleep(10)
            sresult.homew.destroy()
            sresult.awayw.destroy()
            sresult.result.destroy()
            i+=1
            if i==len(home):
                i = 0

    elif value == 'golf':
        local_driver, section = search_sport('golf',query.lower())
        if local_driver == None:
            return
        rank, name, par, today, result, country  = get_results(section, value, local_driver)
        i = 0
        while i<len(rank) and search_1:
            sresult = Golf(frame1,rank[i].text, name[i].text, par[i].text, today[i].text, result[i].text, country[i].et_attribute('title') )
            sresult.create_widgets()
            if not search_1:
                local_driver.quit()
                return
            time.sleep(10)
            sresult.rankw.destroy()
            sresult.countryw.destroy()
            sresult.namew.destroy()
            sresult.parw.destroy()
            i+=1
            if i==len(rank):
                i = 0
        

def search_frame2():
    value = option2var.get().lower()
    global search_2
    search_2 = 1
    query = league2.get()
    query = query.replace(" ","")
    
    if value == 'football':
        local_driver, section = search_sport('football',query.lower())
        if local_driver==None:
            return
        home, away, result = get_results(section, value, local_driver)
        i = 0
        while i<len(home) and search_2:
            r = result[i].text.replace("\n"," ")
            if r!="-" and r!=" - ":
                sresult = Football(frame2, home[i].text, away[i].text, r)
                sresult.create_widgets()
                if not search_2:
                    local_driver.quit()
                    return
                time.sleep(10)
                sresult.home.destroy()
                sresult.away.destroy()
                sresult.result.destroy()
                i+=1
            if i==len(home):
                i = 0

    elif value == 'basketball' or value == 'rugby':
        if value=='basketball':
            local_driver, section = search_sport('basketball',query.lower())
        else :
            local_driver, section = search_sport('rugby',query.lower())
        if local_driver==None:
            return
        home, homescore, away, awayscore  = get_results(section, value, local_driver)
            
        i = 0
        while i<len(home) and search_2:
            if "-" not in homescore[i].text:
                sresult = BasketballRugby(frame2, home[i].text, homescore[i].text, away[i].text, awayscore[i].text)
                sresult.create_widgets()
                if not search_sport:
                    local_driver.quit()
                    return

                time.sleep(10)
                sresult.homew.destroy()
                sresult.awayw.destroy()
                sresult.result.destroy()
                i+=1
            if i==len(home):
                i = 0

    elif value == 'cricket' :
        local_driver, section = search_sport('cricket',query.lower())
        if local_driver==None:
            return
        home, homescore, away, awayscore  = get_results(section, value, local_driver)
        i = 0
        while i<len(home) and search_2:
                

            sresult = Cricket(frame2, home[i].text, homescore[i].text, away[i].text, awayscore[i].text)
            sresult.create_widgets()
            if not search_2:
                local_driver.quit()
                return
            time.sleep(10)
            sresult.homew.destroy()
            sresult.awayw.destroy()
            sresult.result.destroy()
            i+=1
            if i==len(home):
                i = 0

    elif value == 'golf':
        local_driver, section = search_sport('golf',query.lower())
        if local_driver == None:
            return
        rank, name, par, today, result, country  = get_results(section, value, local_driver)
        i = 0
        while i<len(rank) and search_2:

            sresult = Golf(frame2,rank[i].text, name[i].text, par[i].text, today[i].text, result[i].text, country[i].get_attribute('title') )
            sresult.create_widgets()
            if not search_2:
                local_driver.quit()
                return
            time.sleep(10)
            sresult.rankw.destroy()
            sresult.countryw.destroy()
            sresult.namew.destroy()
            sresult.parw.destroy()
            i+=1
            if i==len(rank):
                i = 0

def search_frame3():
    value = option3var.get().lower()
    global search_3
    search_3 = 1
    query = league3.get()
    query = query.replace(" ","")
    
    if value == 'football':
        local_driver, section = search_sport('football',query.lower())
        if local_driver==None:
            return
        home, away, result = get_results(section, value, local_driver)
        i = 0
        while i<len(home) and search_3:
            r = result[i].text.replace("\n"," ")
            if r!="-" and r!=" - ":
                sresult = Football(frame3, home[i].text, away[i].text, r)
                sresult.create_widgets()
                if not search_3:
                    local_driver.quit()
                    return
                time.sleep(10)
                sresult.home.destroy()
                sresult.away.destroy()
                sresult.result.destroy()
                i+=1
            if i==len(home):
                i = 0

    elif value == 'basketball' or value == 'rugby':
        if value=='basketball':
            local_driver, section = search_sport('basketball',query.lower())
        else :
            local_driver, section = search_sport('rugby',query.lower())
        if local_driver==None:
            return
        home, homescore, away, awayscore  = get_results(section, value, local_driver)
            
        i = 0
        while i<len(home) and search_3:
            if "-" not in homescore[i].text:
                sresult = BasketballRugby(frame3, home[i].text, homescore[i].text, away[i].text, awayscore[i].text)
                sresult.create_widgets()
                if not search_sport:
                    local_driver.quit()
                    return

                time.sleep(10)
                sresult.homew.destroy()
                sresult.awayw.destroy()
                sresult.result.destroy()
                i+=1
            if i==len(home):
                i = 0

    elif value == 'cricket' :
        local_driver, section = search_sport('cricket',query.lower())
        if local_driver==None:
            return
        home, homescore, away, awayscore  = get_results(section, value, local_driver)
        i = 0
        while i<len(home) and search_3:
            sresult = Cricket(frame3, home[i].text, homescore[i].text, away[i].text, awayscore[i].text)
            sresult.create_widgets()
            if not search_3:
                local_driver.quit()
                return
            time.sleep(10)
            sresult.homew.destroy()
            sresult.awayw.destroy()
            sresult.result.destroy()
            i+=1
            if i==len(home):
                i = 0

    elif value == 'golf':
        local_driver, section = search_sport('golf',query.lower())
        if local_driver == None:
            return
        rank, name, par, today, result, country  = get_results(section, value, local_driver)
        i = 0
        while i<len(rank) and search_3:
            sresult = Golf(frame3,rank[i].text, name[i].text, par[i].text, today[i].text, result[i].text, country[i].get_attribute('title') )
            sresult.create_widgets()
            if not search_3:
                local_driver.quit()
                return
            time.sleep(10)
            sresult.rankw.destroy()
            sresult.countryw.destroy()
            sresult.namew.destroy()
            sresult.parw.destroy()
            i+=1
            if i==len(rank):
                i = 0

 
def function_search_frame1():
    t = Thread(target=search_frame1,args=())
    t.start()

def function_search_frame2():
    t = Thread(target=search_frame2,args=())
    t.start()

def function_search_frame3():
    t = Thread(target=search_frame3,args=())
    t.start()


def reset_update1():
    global search_1
    search_1 = 0
    t1 = Thread(target=first_results,args=(option1var.get(),))
    t1.start()

def reset_update2():
    global search_2
    search_2 = 0
    t2 = Thread(target=second_results,args=(option2var.get(),))
    t2.start()

def reset_update3():
    global search_3
    search_3 = 0
    t3 = Thread(target=third_results,args=(option3var.get(),))
    t3.start()


def thread_display_data():
    t = Thread(target=display_data,args=())
    t.start()

def check_option():
    value1 = option1var.get()
    value2 = option2var.get()
    value3 = option3var.get()

    value = set((value1, value2, value3))
    if len(value)!=3:
        messagebox.showerror("Error","Select non null unique sports")
    else:
        thread_display_data()
    
def close_app():
    global until_exit
    until_exit = 0
    try:
        root.quit()
        sys.exit()
    except:
        root.destroy()
        sys.exit()

def get_location():
    def location_():
        global city, region
        r = requests.get('http://ipinfo.io/json')
        data = r.json()
        city = data['city']
        region = data['region']
        location.configure(text=region+', '+city)
        dummy_get_weather()
    t10 = Thread(target=location_,args=())
    t10.start()

def set_date():
    def change_data():
        while not until_exit:
            date_now = datetime.now().date()
            date_now = date_now.strftime("%A %d %B %Y")
            date.configure(text=date_now)
            time.sleep(300)
    t11 = Thread(target=change_data,args=())
    t11.start()


def update_time():
    def change_time():
        while  not until_exit:
            time_now  = datetime.now()
            time_label.configure(text=f'{time_now.hour}:{time_now.minute}:{time_now.second}')
            time.sleep(1)
    t12 = Thread(target=change_time,args=())
    t12.start()

def get_weather_details():
    # loc = region+", "+city
    # loc_driver.get('https://www.weatherbug.com/')
    loc_driver.implicitly_wait(3)
    # try :
    #     search_bar = WebDriverWait(loc_driver, 120).until(EC.presence_of_element_located((By.XPATH,"/html/body/div/div[1]/div[3]/div[1]/form/input")))
    # except exceptions.TimeoutException:
    #     loc_driver.refresh()
    #     search_bar = WebDriverWait(loc_driver, 120).until(EC.presence_of_element_located((By.XPATH,"/html/body/div/div[1]/div[3]/div[1]/form/input")))

    # search_bar.send_keys(loc+Keys.RETURN)
    
    while not until_exit  :

        temp, desc = search_by_location(loc_driver)
        if temp!=None and desc!=None:
            weather_desc.configure(text=temp.text+" "+desc.text)
            # print(temp.text+" "+desc.text)
            time.sleep(3000)
            loc_driver.refresh()
 
    

def dummy_get_weather():
    t1 = Thread(target=get_weather_details,args=())
    t1.start()


loc_driver = weather_main()

root = Tk()
root.configure(background="blue")
root.geometry("700x600")

league1= StringVar()
league2 = StringVar()
league3 = StringVar()

twitter_logo = Image.open('twitter.png')
twitter_logo = twitter_logo.resize((30,30))
twitter_logo = ImageTk.PhotoImage(twitter_logo)

bbc_sport_logo  = Image.open('bbc.png')
bb_sport_logo = bbc_sport_logo.resize((30,30),Image.ANTIALIAS)
bbc_sport_logo = ImageTk.PhotoImage(bbc_sport_logo)

espn_logo  = Image.open('espn.png')
bb_sport_logo = espn_logo.resize((30,30),Image.ANTIALIAS)
espn_logo = ImageTk.PhotoImage(espn_logo)

#Frames
login_frame = Frame(root,bg="white")
login_frame.place(relheight=1,relwidth=1)

options_frame = Frame(root,bg='white')
options_frame.place(relwidth=1,relheight=1)

baseframe = ScrollFrame(root)
baseframe.pack(fill='both',expand=1)
baseframe.tkraise()

display = Frame(baseframe.viewPort,bg='white')
display.pack(side='left',anchor=NW,fill='both',expand=1)

twitter_frame = Frame(display,bg='white')
twitter_frame.pack(fill='x',expand=1,ipady=120)
Label(twitter_frame, bg='#03dffc').place(rely=0.93,relx=0.33,relwidth=0.33,height=4)

bbc_frame = Frame(display,bg='white')
bbc_frame.pack(fill='x',expand=1,ipady=70)

espn_frame = Frame(display,bg='white')
espn_frame.pack(fill='x',expand=1,ipady=70)
Label(espn_frame, bg='#03dffc').place(rely=0.95,relx=0.33,relwidth=0.33,height=4)


frame1 = Frame(display,bg='white')
frame1.pack(ipady=250,fill='x',expand=1)
Label(frame1, bg='#03dffc').place(rely=0.93,relx=0.33,relwidth=0.33,height=4)

searchs1 = Entry(frame1,textvariable=league1,borderwidth=1,highlightbackground='black',highlightthickness=2,font=("Arial",13))
searchs1.place(relx=0.17,relwidth=0.25,height=35,y=150)
searchs1.config(state='disabled')

search_button_1 = Button(frame1,text='Search',command=function_search_frame1)
search_button_1.place(relx=0.43,relwidth=0.2,height=35,y=150)
search_button_1.config(state='disabled')

reset_button1 = Button(frame1, text='Reset',command=reset_update1)
reset_button1.place(relx=0.64,relwidth=0.14,height=35,y=150)
reset_button1.config(state='disabled')


frame2 = Frame(display,bg='white')
frame2.pack(ipady=250,fill='x',expand=1)
Label(frame2, bg='#03dffc').place(rely=0.93,relx=0.33,relwidth=0.33,height=4)

searchs2 = Entry(frame2,textvariable=league2,borderwidth=1,highlightbackground='black',highlightthickness=2,font=("Arial",13))
searchs2.place(relx=0.17,relwidth=0.25,height=35,y=150)
searchs2.config(state='disabled')

search_button_2 = Button(frame2,text='Search',command=function_search_frame2)
search_button_2.place(relx=0.43,relwidth=0.2,height=35,y=150)
search_button_2.config(state='disabled')

reset_button2 = Button(frame2, text='Reset',command=reset_update2)
reset_button2.place(relx=0.64,relwidth=0.14,height=35,y=150)
reset_button2.config(state='disabled')

frame3 = Frame(display,bg='white')
frame3.pack(ipady=250,fill='x',expand=1)
Label(frame3, bg='#03dffc').place(rely=0.93,relx=0.33,relwidth=0.33,height=4)

searchs3 = Entry(frame3,textvariable=league3,borderwidth=1,highlightbackground='black',highlightthickness=2,font=("Arial",13))
searchs3.place(relx=0.17,relwidth=0.25,height=35,y=150)
searchs3.config(state='disabled')

search_button_3 = Button(frame3,text='Search',command=function_search_frame3)
search_button_3.place(relx=0.43,relwidth=0.2,height=35,y=150)
search_button_3.config(state='disabled')

reset_button3 = Button(frame3, text='Reset',command=reset_update3)
reset_button3.place(relx=0.64,relwidth=0.14,height=35,y=150)
reset_button3.config(state='disabled')


frame4 = Frame(display,bg='white')
frame4.pack(ipady=300,fill='x',expand=1)

time_label = Label(frame4,bg='white',font=("Arial",13))
time_label.place(relx=0.35,rely=0.1,relwidth=0.3)
update_time()

date = Label(frame4,bg='white',font=("Arial",13))
date.place(relx=0.35, rely=0.15,relwidth=0.3)
set_date()

location = Label(frame4,bg='white',font=("Arial",13))
location.place(relx=0.35,rely=0.25,relwidth=0.3)
get_location()

weather_desc = Label(frame4,bg='white',font=("Arial",13))
weather_desc.place(relx=0.3,rely=0.35,relwidth=0.4)
# dummy_get_weather()

exit_button = Button(frame4, text='EXIT',bg='white',highlightcolor='black',command=close_app)
exit_button.place(relx=0.4,rely=0.9,relwidth=0.2,height=40)


Label(twitter_frame,image=twitter_logo,compound='center',bg='white').pack()
Label(bbc_frame, image=bbc_sport_logo, compound='center',bg='white',height=30,width=30).pack()
Label(espn_frame,image=espn_logo,compound='center',bg='white').pack()

login_frame.tkraise()
# options_frame.tkraise()

root.wm_title("Twitter | Login")

#variables
username = StringVar()
password = StringVar()
option1var = StringVar(value="None")
option2var = StringVar(value="None")
option3var = StringVar(value="None")
#Login Widgets
Label(login_frame,text="LOGIN TO TWITTER",bg='white',fg="#03c6fc",activeforeground="#0373fc",font=("Dubai Mediam",25,"bold")).place(relx=0.3,rely=0.13)
user = Entry(login_frame,textvariable=username,borderwidth=1,highlightbackground='black',highlightthickness=2,font=("Arial",13))
passwd = Entry(login_frame,textvariable=password,borderwidth=1,show="*",highlightbackground='black',highlightthickness=2,font=("Arial",13))

Label(login_frame,text="USERNAME :",font=("Arial",17),bg='white').place(relx=0.2,rely=0.4)
Label(login_frame,text="PASSWORD :",font=("Arial",17),bg='white').place(relx=0.2,rely=0.5)

user.place(relx=0.5,rely=0.4,width=200,height=40)
passwd.place(relx=0.5,rely=0.5,width=200,height=40)

login_button = Button(login_frame,text="LOGIN",font=("Arial",20),bg='white',command=options_raise)
login_button.place(relx=0.4,rely=0.8,width=150,height=40)

#Options Frame

Label(options_frame, text='Select Sports',bg='white',font=('Arial',15),anchor=CENTER).place(relx=0.35,rely=0.1,relwidth=0.3)
options = ["None", "Football", "Basketball", "Rugby", "Cricket",  "Golf", "Boxing"]
option1 = ttk.OptionMenu(options_frame,option1var,*options,)
option2 = ttk.OptionMenu(options_frame,option2var,*options,)
option3 = ttk.OptionMenu(options_frame,option3var,*options,)
option1.place(relx=0.3,rely=0.4)
option2.place(relx=0.6,rely=0.4)
option3.place(relx=0.45,rely=0.6)

next_button = Button(options_frame,text='Next',command=check_option,borderwidth=1,highlightbackground='black',highlightthickness=2,font=("Arial",13))
next_button.place(relx=0.45,rely=0.8,relwidth=0.1)


#display frame
root.mainloop()
sys.exit()
