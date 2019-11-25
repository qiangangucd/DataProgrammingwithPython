# Week 12 - Assessed exercises

# This week we learnt some advanced data manipulation methods, about APIs and
# about webscraping. In this last set of assessed exercises you must complete the
# Brightspace quiz 'W12 - Assessed exercises' and submit a .py file with the 
# code you used to answer the questions in your quiz. Each question is work
# 0.5 marks and it is either correct (full marks) or incorrect (0 marks).

# This template file contains code that will help you answer the questions in 
# the quiz.

# Q1 and Q2 are based on the advanced data manipulation section. You will need to 
# use the titantic dataset which is part of the seaborn package and can be loaded
# using the following commands
import seaborn as sb

titanic = sb.load_dataset('titanic')
# The questions involve using the groupby function and applying functions to that
# grouped object. For questins involving the interquartile range, use the function
# from lecture_12_code.py

# Q1
age_male_sur_mean = round(titanic.age[titanic.sex == 'male'][titanic.survived == 1].mean())
print('age_male_survived_mean:', age_male_sur_mean)
# Q2
fare_male_sur_std = round(titanic.fare[titanic.sex == 'male'][titanic.survived == 1].std())
print('fare_male_survived_std:', fare_male_sur_std)

# Q3 to Q5 relate to the World Bank API. You will be asked to search of indicator
# and country codes in Q3 and Q4. In Q5 you will need to extract data from the 
# the World Bank for a particular indicator, country and year
import wbdata as wbd
from datetime import datetime


# Q3
def IQR(x):
    return x.quantile(0.75) - x.quantile(0.25)


age_female_sur_quan = round(titanic.age[titanic.sex == 'female'][titanic.survived == 1].agg(IQR))
print('age_female_survived_quartile:', age_female_sur_quan)

# Q4
country_code = wbd.search_countries('Indonesia')[0]['id']
print('country code:', country_code)

# Q5
indicator = {'SH.STA.OWAD.ZS': 'prevalence of overweight'}
per = round(wbd.get_dataframe(indicator, wbd.search_countries('Ireland')[0]['id'], datetime(2010, 1, 1)).iloc[0][0])
print('the prevalence of overweight adults:', per)

# Q6 to Q8 relate to webscraping and uses the Spotify weekly charts. You will need
# to import BeautifulSoup and the requests package
from bs4 import BeautifulSoup
import requests
import re
import numpy as np

# The below code loads the data from the Spotify weekly charts for the week
# 2017-06-30 to 2017-07-07, and uses BeautifulSoup to parse the html.
spotify = requests.get('https://spotifycharts.com/regional/global/weekly/2017-06-30--2017-07-07')
soup = BeautifulSoup(spotify.text, "html.parser")

# The following commands extract the information related to the tracks and removes
# the html tags
track = soup.find_all('td', class_="chart-table-track")
tracks = [x.text.strip() for x in track]
# Q6 asks you to search through tracks to find the number of times a particular
# arist appears in this weekly chart
counts = len(
    [e for e in [re.findall(r'Justin Bieber', tracks[i].replace('\n', ' ')) for i in range(len(tracks))] if e != []])
print('the number of Justin Bieber appears:', counts)

# The following commands extract the information related to the number of plays,
# removes the html tags and commas, and converts the value to an integers
play = soup.find_all('td', class_="chart-table-streams")
plays = [int(x.text.strip().replace(',', '')) for x in play]
# Q7 asks you to perform some statistical analysis on these numbers

num_plays = round(np.mean(plays))
print('means:', num_plays)

# Q8 asks you to load the charts for a different week and determine how many of
# the songs from the original week 2017-06-30 to 2017-07-07 are still in the 
# charts at this later week. To load in the data for the new week, change the
# date range in the url to the date range specified in your question.
spotify2 = requests.get('https://spotifycharts.com/regional/global/weekly/2018-06-29--2018-07-06')
soup2 = BeautifulSoup(spotify2.text, "html.parser")

song1 = soup.find_all('strong')
songs1 = [x.text for x in song1]
song2 = soup2.find_all('strong')
songs2 = [x.text for x in song2]

count = 0
for e1 in songs1:
    for e2 in songs2:
        if e1 == e2:
            count += 1

print('counts:', count)
