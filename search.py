from results import get_golf, get_basketball, get_rugby, get_score_block, get_results, get_football, get_cricket

football = {
    'premier-league':'https://www.flashscore.co.uk/football/england/premier-league/results/',
    'championship':'https://www.flashscore.co.uk/football/england/championship/results/',
    'league one':'https://www.flashscore.co.uk/football/england/league-one/results/',
    'league two':'https://www.flashscore.co.uk/football/england/league-two/results/',
    'eflcup':'https://www.flashscore.co.uk/football/england/efl-cup/results/',
    'efltrophy':'https://www.flashscore.co.uk/football/england/efl-trophy/results/',
    'facup':'https://www.flashscore.co.uk/football/england/fa-cup/results/',
    'bundesliga':'https://www.flashscore.co.uk/football/germany/bundesliga/results/',
    'ligue1':'https://www.flashscore.co.uk/football/france/ligue-1/results/',
    'seriea':'https://www.flashscore.co.uk/football/italy/serie-a/results/',
    'premiership':'https://www.flashscore.co.uk/football/scotland/premiership/reults/',
    'laliga':'https://www.flashscore.co.uk/football/spain/laliga/results/',
    'euro':'https://www.flashscore.co.uk/football/europe/euro/results/',
    'championsleague':'https://www.flashscore.co.uk/football/europe/champions-league/results/',
    'europaleague':'https://www.flashscore.co.uk/football/europe/europa-league/results/',
    'worldcup':'https://www.flashscore.co.uk/football/world/world-cup/results/',
    'olympicgames':'https://www.flashscore.co.uk/football/world/olympic-games/results/',
    'fifaclubworldcup':'https://www.flashscore.co.uk/football/world/olympic-games/results/',
}

cricket = {
    'bigbashleague':'https://www.flashscore.co.uk/cricket/australia/big-bash-league/results/',
    'ipl':'https://www.flashscore.co.uk/cricket/india/ipl/results/',
    'countychampionshipone':'https://www.flashscore.co.uk/cricket/united-kingdom/county-championship-one/results/',
    'thehundred':'https://www.flashscore.co.uk/cricket/united-kingdom/the-hundred/results/',
    'vitalityblast':'https://www.flashscore.co.uk/cricket/united-kingdom/vitality-blast/results/',
    'onedaycup':'https://www.flashscore.co.uk/cricket/united-kingdom/one-day-cup/results/',
    'testseries':'https://www.flashscore.co.uk/cricket/world/test-series/results/',
    'oneday':'https://www.flashscore.co.uk/cricket/world/one-day-international/results/',
    'twenty20':'https://www.flashscore.co.uk/cricket/world/twenty20-international/results/'

}

golf = {
    'usopen':'https://www.flashscore.co.uk/golf/pga-tour/us-open/',
    'pgachampionship':'https://www.flashscore.co.uk/golf/pga-tour/pga-championship/',
    'olympic':'https://www.flashscore.co.uk/golf/others-men/olympic-games/',
    'masterstournament':'https://www.flashscore.co.uk/golf/pga-tour/masters-tournament/',
    
}

basketball = {
    'lnb':'https://www.flashscore.co.uk/basketball/france/lnb/results/',
    'legaa':'https://www.flashscore.co.uk/basketball/italy/lega-a/results/',
    'acb':'https://www.flashscore.co.uk/basketball/spain/acb/results/',
    'superlig':'https://www.flashscore.co.uk/basketball/turkey/super-lig/results/',
    'bbl':'https://www.flashscore.co.uk/basketball/united-kingdom/bbl/results/',
    'olympic':'https://www.flashscore.co.uk/basketball/world/olympic-games/results/',
    'championsleague':'https://www.flashscore.co.uk/basketball/europe/champions-league/results/',
    'eurocup':'https://www.flashscore.co.uk/basketball/europe/eurocup/results/',
    'euroleague':'https://www.flashscore.co.uk/basketball/europe/euroleague/results/',
    'eurobasket':'https://www.flashscore.co.uk/basketball/europe/eurobasket/results/',
    'nba':'https://www.flashscore.co.uk/basketball/usa/nba/results/'

}

rugby = {
    'premiershiprugby':'https://www.flashscore.co.uk/rugby-union/england/premiership-rugby/results/',
    'top14':'https://www.flashscore.co.uk/rugby-union/france/top-14/',
    'sixnations':'https://www.flashscore.co.uk/rugby-union/europe/six-nations/results/',
    'europeanrugbychampionscup':'https://www.flashscore.co.uk/rugby-union/europe/european-rugby-champions-cup/results/',
    'worldcup':'https://www.flashscore.co.uk/rugby-union/world/world-cup/results/',
    'superrugby':'https://www.flashscore.co.uk/rugby-union/world/super-rugby/results/',
    'olympic':'https://www.flashscore.co.uk/rugby-union/world/olympic-games-7-s/results/'

}



def search_sport(sport,query):
    driver, section = None, None
    if sport=='football':
        if query in football.keys():
            link = football[query]
            driver, section = get_football(link)

    elif sport=='basketball':
        if query in basketball.keys():
            link = basketball[query]
            driver, section = get_basketball(link)
    
    elif sport=='rugby':
        if query in rugby.keys():
            link = rugby[query]
            driver, section = get_rugby(link)

    elif sport=='golf':
        if query in golf.keys():
            link = golf[query]
            driver, section = get_golf(link)

    elif sport=='cricket':
        if query in cricket.keys():
            link = cricket[query]
            driver, section = get_cricket(link)

    return driver, section
    