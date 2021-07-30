from typing import Optional
import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
# print(driver.title)
import time
from tweets import TwitterCards

from tkinter import *

root = Tk()
root.geometry("300x300")
dummy_frame = Frame(root)
dummy_frame.place(relheight=1,relwidth=1)

canvas = Canvas(dummy_frame)
canvas.place(relwidth=1,relheight=1)

display_frame = Frame(canvas,bg='red')

Label(display_frame,text='lol').pack()
y_scrollbar  = Scrollbar(dummy_frame, orient="vertical",command=canvas.yview)
y_scrollbar.pack(side=RIGHT,fill=Y)
canvas.configure(yscrollcommand=y_scrollbar.set)
canvas.create_window((0,0),window=display_frame,anchor='nw',width=300)
canvas.bind('<Configure>',lambda e: canvas.configure(scrollregion = canvas.bbox('all')))
# display_frame.pack(fill='both')
y = 100

time.sleep(2)

for i in range(100):
    f= Frame(display_frame,bg='blue',width=200)
    f.pack(fill=X)
    Label(f,text="LOL\n\n\n").pack()
    y+=1


Label(display_frame,text="HI",bg="red")
root.mainloop()

"""
    end_of_scroll_region = False
    last_position = None
    counts = 0
    frame = display_frame
    unique_tweets = set()
    dummy_frame.tkraise()
    

    while not end_of_scroll_region:
        cards = twitter_data(driver)
        

        root.wm_title("Twitter | Home")
        # display_frame.tkraise()
        for card in cards:
            try:
                tweet = extract_data(card)
                if not tweet:
                    continue
                else:
                    tweet_id = generate_tweet_id(tweet)
                    if tweet_id not in unique_tweets and isinstance(tweet,Iterable):
                        print(tweet)
                        f = Frame(display_frame,height=300,bg='white')
                        # f.pack(side=TOP,fill=X,expand=1)
                        f.pack(fill=X)
                        unique_tweets.add(tweet_id)
                        t = TwitterCards(f, tweet, y,root)
                        thread_tweet = Thread(target=t.create_card,)
                        thread_tweet.start()
                        # t.create_card()
                        counts+=1
                        y+=100
            except exceptions.StaleElementReferenceException:
                continue
            
        if counts>1000:
            end_of_scroll_region = True
            break

        last_position, end_of_scroll_region = scroll_down_page(driver, last_position)
        end_of_scroll_region = False
    # driver.quit()
    y = 100
"""

"""
dummy_frame = Frame(root,bg='white')
dummy_frame.place(relheight=1,relwidth=1)

canvas = Canvas(dummy_frame,bg='white')
canvas.place(relwidth=1,relheight=1)

display_frame = Frame(canvas,bg='white')

y_scrollbar  = Scrollbar(dummy_frame, orient="vertical",command=canvas.yview)
y_scrollbar.pack(side=RIGHT,fill=Y)
canvas.configure(yscrollcommand=y_scrollbar.set)
canvas.create_window((0,0),window=display_frame,anchor='nw',width=700)
canvas.bind('<Configure>',lambda e: canvas.configure(scrollregion = canvas.bbox('all')))
display_frame.bind("<Configure>", reset_scrollregion)
# display_frame.pack(side=TOP,fill='both')
"""