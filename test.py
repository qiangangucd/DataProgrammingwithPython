import pandas as pd
import numpy as np

# data=pd.read_csv('diamonds_4.csv')
# my_missing_2 = {'cut':'-1','clarity':'NaN', 'price':['NULL','-999'],'y':'NaN'}
# my_missing = ['NA','NULL','-999','-1','58']
# dia_5a = pd.read_csv('diamonds_4.csv', na_values=my_missing)
movies = pd.read_csv('movies.dat',sep='::',names=['movie_id','title','genres'])