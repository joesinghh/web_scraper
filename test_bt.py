from requests_html import AsyncHTMLSession
from collections import defaultdict
import pandas as pd 


url = 'https://www.flashscore.co.uk'

asession = AsyncHTMLSession()

async def get_scores():
    r = await asession.get(url)
    await r.html.arender()
    return r

def get_results():

    results = asession.run(get_scores)

    results = results[0]
    times = results.html.find("div.event__time")
    home_teams = results.html.find("div.event__participant.event__participant--home") 
    scores = results.html.find("div.event__scores")
    away_teams = results.html.find("div.event__participant.event__participant--away")
    print(home_teams[0])

    dict_res = defaultdict(list)
    # for ind in range(len(times)):
    #     dict_res['home_teams'].append(home_teams[ind].text)
    #     dict_res['scores'].append(scores[ind].text)
    #     dict_res['away_teams'].append(away_teams[ind].text)

    return dict_res

if __name__=='__main__':
    print(get_results())