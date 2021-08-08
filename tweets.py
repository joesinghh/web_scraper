from data import twitter_data
from tkinter import *
from datetime import datetime

class TwitterCards(object):

    def __init__(self, frame, tweet_data, y,master):
        self.frame = frame
        self.data = tweet_data
        self.y_value = y
        self.master = master
    def create_card(self):
        user, handle, postdate, text, reply_count,retweet_count, likes = self.data
        count_lines = text.count("\n")
        text = text.replace("\n","")
        date = postdate.split("T")[0]
        date = datetime.strptime(date,"%Y-%m-%d").date()
        date = date.strftime("%d%b%Y")
        self.user = Text(self.frame, wrap=WORD,exportselection=False,height=count_lines+3,relief='flat')
        self.user.insert(END, user)
        self.user.place(relx=0,relwidth=0.2,y=40)
        self.user.configure(state='disabled')

        self.tweet_text = Text(self.frame,wrap=WORD,exportselection=False,height=count_lines+3,relief='flat')
        self.tweet_text.insert(END,text)
        self.tweet_text.place(relx=0.22,relwidth=0.75,y=40,relheight=0.7)
        self.tweet_text.configure(state='disabled')
        self.master.update()

