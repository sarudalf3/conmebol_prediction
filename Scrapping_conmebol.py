import requests
from bs4 import BeautifulSoup 
import pandas as pd
from urllib.request import urlopen

from datetime import datetime
import calendar
monthdict={v: k for k,v in enumerate(calendar.month_name)} #create the dictionary with name months and its number

import warnings
warnings.filterwarnings("ignore") #Ignore warnings

def Qualifiers_WC_Scrapping(url, year, other=True):
    website = requests.get(url)
    html = urlopen(url) #open the url
    soup = BeautifulSoup(html,'html.parser') #save the page source

    dates = soup.find_all('div', {'class':'fdate'}) #select tag div with class fdate
    homes = soup.find_all('th', {'class':'fhome'}) #select tag th with class fhome
    scores = soup.find_all('th', {'class':'fscore'}) #select tag th with class fscore
    aways = soup.find_all('th', {'class':'faway'}) #select tag th with class faway

    date = []
    for d in dates:
        date.append(d.get_text()) #get the text in the tag

    home = []    
    for h in homes:
        home.append(h.get_text()) #get the text in the tag

    score = []    
    for s in scores:
        score.append(s.get_text()) #get the text in the tag

    away = []    
    for a in aways:
        away.append(a.get_text()) #get the text in the tag

    if year==2022:
        date = date[:-1]
        home = home[:-1]
        score = score[:-1]
        away = away[:-1]

    day = pd.DataFrame(date, columns=['Date text'])
    day['Date text'] = day['Date text'].str.replace("\[note 1\]","", case=True) #replace cases


    if other == False: #get the game date
        day['day'] = day['Date text'].apply(lambda x:int(x[-3:-1]))
        day['month'] = day['Date text'].apply(lambda x:int(x[-6:-4]))
        day['year'] = day['Date text'].apply(lambda x:int(x[-11:-7]))
    elif other==True:
        day['split'] = day['Date text'].str.split(' ')
        day['day'] = day['split'].apply(lambda x:x[0])
        day['month'] = day['split'].apply(lambda x:x[1])
        day['year'] = day['split'].apply(lambda x:x[2])
        day.replace({'month': monthdict}, inplace=True)

    day['date'] =  pd.to_datetime(day[['year', 'month', 'day']], format='%d-%m-%y')
    day.loc[:,'World Cup Qualif'] = year

    home = pd.DataFrame(home, columns=['Team_home']) #get the home teams
    home['Team_home'] = home['Team_home'].str.strip()
    away = pd.DataFrame(away, columns=['Team_away']) #get the away teams
    away['Team_away'] = away['Team_away'].str.strip()

    score = pd.DataFrame(score, columns=['Goals']) #get the final score
    score = score[~score['Goals'].isin(['v','Suspended[note 4]','Abandoned[note 4]'])]
    
    score['Goals_home'] = score['Goals'].apply(lambda x:x[0])
    score['Goals_away'] = score['Goals'].apply(lambda x:x[2])

    score['Goals_home'] = pd.to_numeric(score['Goals_home'])
    score['Goals_away'] = pd.to_numeric(score['Goals_away'])

    WC_qual = pd.concat([day, home, away, score], axis=1) #concat in a dataframe
    cols = ['date','World Cup Qualif','Team_home','Team_away','Goals_home','Goals_away'] #select this columns
    return WC_qual[cols]

#wikipedia website for 1908 World Cup
url_1998 = "https://en.wikipedia.org/wiki/1998_FIFA_World_Cup_qualification_(CONMEBOL)"
WC_1998 = Qualifiers_WC_Scrapping(url_1998, year=1998, other=True)
#WC_1998['World Cup Qualif'] = 1998

#wikipedia website for 2002 World Cup
url_2002 = "https://en.wikipedia.org/wiki/2002_FIFA_World_Cup_qualification_(CONMEBOL)"
WC_2002 = Qualifiers_WC_Scrapping(url_2002, year=2002, other=True)
#WC_2002['World Cup Qualif'] = 2002

#wikipedia website for 2006 World Cup
url_2006 = "https://en.wikipedia.org/wiki/2006_FIFA_World_Cup_qualification_(CONMEBOL)"
WC_2006 = Qualifiers_WC_Scrapping(url_2006, year=2006, other=True)
#WC_2006['World Cup Qualif'] = 2006

#wikipedia website for 2010 World Cup
url_2010 = "https://en.wikipedia.org/wiki/2010_FIFA_World_Cup_qualification_(CONMEBOL)"
WC_2010 = Qualifiers_WC_Scrapping(url_2010, year=2010, other=True)
#WC_2010['World Cup Qualif'] = 2010

#wikipedia website for 2014 World Cup
url_2014 = "https://en.wikipedia.org/wiki/2014_FIFA_World_Cup_qualification_(CONMEBOL)"
WC_2014 = Qualifiers_WC_Scrapping(url_2014, year=2014, other=True)
#WC_2014['World Cup Qualif'] = 2014

#wikipedia website for 2018 World Cup
url_2018 = "https://en.wikipedia.org/wiki/2018_FIFA_World_Cup_qualification_(CONMEBOL)"
WC_2018 = Qualifiers_WC_Scrapping(url_2018, year=2018, other=False)
#WC_2018['World Cup Qualif'] = 2018

#wikipedia website for 2022 World Cup
url_2022 = "https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_qualification_(CONMEBOL)"
WC_2022 = Qualifiers_WC_Scrapping(url_2022, year=2022, other=False)
#WC_2022['World Cup Qualif'] = 2022

database = pd.concat([WC_1998, WC_2002, WC_2006, WC_2010, WC_2014, WC_2018, WC_2022], axis=0, ignore_index=True)
cols = ['date','World Cup Qualif','Team_home','Team_away','Goals_home','Goals_away']
database = database[cols]

del url_1998, WC_1998, url_2002, WC_2002, url_2006, WC_2006, url_2010, WC_2010 #delete variables 
del url_2014, WC_2014, url_2018, WC_2018, url_2022, WC_2022, monthdict, cols #delete variables

#database.to_hdf('conmebol.h5', key='df', mode='w')