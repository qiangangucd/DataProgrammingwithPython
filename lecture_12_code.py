# -*- coding: utf-8 -*-
# Lecture 12 code - Advanced Python wrangling, Web scraping, Accessing APIs

# Useful resources:
# 
# Chapter 9 of McKinney
# www.codecademy.com - Introduction to APIs in Python
# http://www.pythonforbeginners.com/api/list-of-python-apis - list of Python APIs
# http://www.gregreda.com/2013/03/03/web-scraping-101-with-python/ - web scraping with Python
# http://wbdata.readthedocs.org/en/latest/ - World bank API
# http://www.crummy.com/software/BeautifulSoup/bs4/doc/ - Use of beautifulsoup package

from pandas import Series, DataFrame
import pandas as pd
import numpy as np

################################################################################

# Chapter 9 of McKinney

# Idea: Split, Apply, Combine
# Split the data up by one or more keys
# Apply some function to the different bits
# Combine it all back together

tips = pd.read_csv('https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/master/csv/reshape2/tips.csv')

# Data set comes from the R reshape2 package - see also references therein
# Contains a load restaurant bills wiht the tip, the sex of the payee, whether
# they smoked, the day, the time, and the size of the party

# Have a look at it:
tips.head()

# Create a new column containing the percentage tip
tips['pct'] = tips.tip/tips.total_bill

# Suppose I now want to see whether males or females tip more on average
# One way of doing it
tips.pct[tips.sex=='Female'].mean()
tips.pct[tips.sex=='Male'].mean()
# Females tip slightly more

# A more elegant way is to create a grouped by object
tips_gr = tips.pct.groupby(tips.sex)
# This doesn't contain anything obvious:
tips_gr

# But now you can access things with it:
tips_gr.mean()
tips_gr.std()
# Other functions you can use include count, sum , median, min/max, etc
# See tips_gr.<Tab> for lots more

# If you're interested in multiple variables you can do this too
tips_gr_2 = tips.groupby('sex')
tips_gr_2.median()

# You don't have to group by just one variable
tips_gr_3 = tips.groupby(['sex','smoker'])
tips_gr_3.describe()
tips_gr_3.mean()

# Note that tips_gr_3 has a hierarchical index of both smoker and sex
# You can get re-arrange this with
tips_gr_3.mean().unstack()
# or
tips_gr_3.mean().unstack(level=0)
# Note the difference, the first adds smoker to the columns whilst the second
# adds sex - both are still hierarchical indexes

# Unstack is often more useful if you have just one variable with a hierarchical
# index:
tips_gr_4 = tips.pct.groupby([tips.sex,tips.smoker])
tips_gr_4.mean()
tips_gr_4.mean().unstack() # Turns it into a nice DataFrame with no hierarchical index

# You can actually pass any Series function to a grouped by object
def IQR(x):
    return x.quantile(0.75)-x.quantile(0.25)
    
# You just need to provide it to the agg method
tips.groupby(['sex','smoker']).agg(IQR)

# You can use agg to get fancier tables of results
tips.groupby(['sex','smoker']).agg(['count','mean','std'])

# You can even run different functions for different columns by providing a dict
tips.groupby(['sex','smoker']).agg({'total_bill':'count','tip':'mean','size':'std'})

# Or even more complicated!
tips.groupby(['sex','smoker']).agg({'total_bill':'count','tip':['mean','min','max'],'size':'std'})

# Much more to cover here, including transform and pivot_tables but we've run out of time

################################################################################

## APIs

# We're going to work with a few packages that load in the API for us
# See www.codecademy.com - Introduction to APIs in Python for more examples

# First up the world bank - two packages wbpy and wbdata - we'll use wbdata
# More docs at http://wbdata.readthedocs.org/en/latest/
import wbdata as wbd

# Example 1: Get total population from Ireland from 1960 to 2012
country1 = ['IE'] # Needs to be a proper country code in a list
indicator1 = {'SP.POP.TOTL':'Total Population'} # Needs to be a pre-defined variable name in a dict
# Gives data in reverse order by default
data1 = wbd.get_dataframe(indicator1,country1).sort_index()
data1.head()
data1.plot() 
 
 # This is fine but what if you need to find different countries?
wbd.get_country()
# Too long a list, easier to search 
wbd.search_countries('South')

# What if you want to get different indicators
#wbd.get_indicator() # Too slow
wbd.search_indicators('GDP') # Too many!

# Perhaps instead look by source
wbd.get_source()
# or topic
wbd.get_topic()
# Now search
wbd.search_indicators('CO2',topic=19) 

# What about getting multiple countries
country2 = ['IE','US','CN'] # Ireland, USA, China
indicator2 = {'EN.ATM.CO2E.KT':'CO2 emissions (kt)'}

# Get the data
data2 = wbd.get_dataframe(indicator2,country2).sort_index()
# Need to unstack to get this into proper order
data2_u = data2.unstack(level=0)
data2_u.head()
data2_u.plot()

# Can do multiple indicators too
country3 = ['US','CN'] # US, China
indicator3 = {'EN.ATM.CO2E.PC':'CO2 emmissions','SP.POP.GROW':'Population growth (annual %)'}
data3 = wbd.get_dataframe(indicator3,country3).sort_index().unstack(level=0)
data3.head()

# Create one of my favourite plots: 
import datetime
# health expenditure per capita vs life expectancy
OECD = ['AUS', 'AUT', 'BEL', 'CAN', 'CH', 'CHL', 'CZE', 'DEU', 'DNK', 'ESP',
       'EST', 'FIN', 'FRA', 'GBR', 'GRC', 'HUN', 'IRL', 'ISL', 'ISR',
       'ITA', 'JPN', 'KOR', 'LV','LUX', 'MEX', 'NLD', 'NOR', 'NZL',
       'POL', 'PRT', 'SVK', 'SWE', 'TUR', 'USA']
indicator4 = {"SH.XPD.CHEX.PP.CD": "Health expenditure", "SP.DYN.LE00.IN": "Life expectancy"}
data_date4 = (datetime.datetime(2009, 1, 1), datetime.datetime(2009,12,31))   
data4 = wbd.get_dataframe(indicator4,OECD,data_date4)
data4.head()

import matplotlib.pyplot as plt
plt.figure()
plt.plot(data4.iloc[:,0], data4.iloc[:,1],'.')
plt.axis([0, 8000, 70, 85])
plt.xlabel('Health expenditure per capita (USD)')
plt.ylabel('Life expectancy at birth, total (years)')
plt.title('Scatter plot of health expenditure per capita vs Life expectancy in 2009')
plt.grid(b=True, which='major', color='0.6', linestyle=':')
n = data4.shape[0]
country_labelled = ['MEX','KOR','HUN','GBR','JPN','USA']
for j in range(len(country_labelled)):
    i = OECD.index(country_labelled[j])
    plt.text(data4.iloc[i,0], data4.iloc[i,1], data4.index[i])
    
# Compare with this: http://www.forbes.com/sites/danmunro/2012/12/30/2012-the-year-in-healthcare-charts/
# Looks slightly different?

################################################################################

# APIs 2: wikipedia
# See https://wikipedia.readthedocs.org/en/latest/quickstart.html
# and https://wikipedia.readthedocs.org/en/latest/code.html#api

# Install with pip install wikipedia
import wikipedia as wp

# Search
wp.search('Ireland')

# Use the results tag to get fewer results (sorted by popularity?)
wp.search('Ireland',results=5)

# Get the summary
wp.summary('Ireland')
wp.summary('Ireland',sentences=1)

# Get a full page
Dublin = wp.page('Dublin')
Dublin.title
Dublin.url
Dublin.content
Dublin.images
Dublin.links

# Geosearch searches by latitude
wp.geosearch(48.8582,2.2945,radius=100)

# Get a random page
wp.random(pages=1)

# Get the raw html
Dublin_raw = wp.WikipediaPage('Dublin')
Dublin_raw.html() # Slow
# Can get way more rich stuff with this too, including revision IDs and similar

# Some fun ideas
# Find two random pages and see if you can link them together via intermediate pages using the links object
# Create a social network matrix of articles that link to each other
# Use regular expressions to extract interesting bits of text from pages. e.g. what's the most popular word used on wikipedia?
# Any other good ideas?

###############################################################################

# Web scraping: the wonderful beautifulsoup
# See http://www.crummy.com/software/BeautifulSoup/bs4/doc/ 

# To use this properly you really need to know some html
# Try the html/css courses at codecademy.com

# Install with pip install beautifulsoup4
# import 
import requests
from bs4 import BeautifulSoup
# requests was already installed on my machine, but you might need to install it too

# So simple to use: give it a website
page = requests.get('https://www.irishtimes.com/').text
soup = BeautifulSoup(page, 'html.parser')

# Make the html look nice
print(soup.prettify())

# Now print bits of it out
soup.title # The title

# Print out the text
soup.get_text()

# Find all the links
soup.find_all('a')

# Find all the headers
soup.find_all('h2')

# Find all the big headlines
soup.find_all('span',class_='h2')
# Find all the smaller headlines
soup.find_all('span',class_='h4')
# Use regular expression to return both all span's of class h_
import re
soup.find_all('span',class_=re.compile(r'h[0-9]+'))

# Find the most read headlines
soup.find_all('span',class_='tr-headline')

# Find the links to all news stories
soup.find_all('a', attrs={'data-category':"News"})
# Could now do some regular expression magic to get the stories and/or links out
soup.find_all('div', class_=re.compile('.*headline*'))

# Now think of all the fantastic uses you could have for this:
# Downloading loads of product pages from e.g. amazon and others, and comparing prices
# Looking at changing news stories over time by e.g. key words
# Automatically finding house prices as advertised by estate agents and comparing them to the price sold on the property price register
# etc etc
