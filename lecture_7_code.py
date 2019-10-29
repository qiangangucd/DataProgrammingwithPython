# Code for lecture 7 - A little bit more on loading/saving data with pandas and then on to some more data wrangling stuff

## Loading data with pandas - chapter 6 of McKinney
# We already met back in lecture 1 the pandas function read_csv, whilst in lecture 4 we covered the basic Python methods for loading in data
# Here we'll cover the other pandas methods
# We going to use small examples of the Diamonds data, called diamonds_1.csv, diamonds_2.csv, etc

# Short description of these data sets (load them up in Excel or Notepad or whatever if you want to verify the shapes of these)
# diamonds_1.csv is just a csv file with header rows and nothing complicated - hopefully all your data sets are like this. 
# """"""""_2.csv is the same but without the header
# """"""""_3.csv is the same as diamonds_1 but contains some junk at the top
# """"""""_4.csv is the same as diamonds_1 but contains some weird missing values

# Load in packages
from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import numpy.random as npr

# It will help to set a path for this set of code
# path = "/Volumes/GoogleDrive/My Drive/STAT40800/Week7/Code/"
#
# # Basics of read_csv
# # Read in diamonds_1.csv
# dia_1 = pd.read_csv(path+'diamonds_1.csv')
# # If the seperator s not a comma you should specify it using sep
# dia_1a = pd.read_csv(path+'diamonds_1.csv',sep=',')
# # The sep command can also be something fancy like a regular expression
#
# # Files missing a header with header=None - note the default integer index on the columns
# dia_2 = pd.read_csv(path+'diamonds_2.csv',header=None)
#
# # Specifying the index manually using names argument
# dia_2a = pd.read_csv(path+'diamonds_2.csv',header=None,names=list('abcdefghij'))
#
# # Incorporate the index from a column using index_col
# dia_2b = pd.read_csv(path+'diamonds_1.csv',index_col='cut')
# # Note: non-unique index
#
# # Skip rows with skiprows - can be a list or an integer (i.e. number of rows to skip)
# dia_3 = pd.read_csv(path+'diamonds_3.csv',skiprows=[0,2,3])
#
# # Reading in small chunks of the file with nrows - useful for big files
# dia_4 = pd.read_csv(path+'diamonds_1.csv',nrows=5)
#
# # Reading in missing values with na_values (input as a dict)
# my_missing = ['NA','NULL','-999','-1']
# dia_5 = pd.read_csv(path+'diamonds_4.csv',na_values=my_missing)
# # If there are different missing values for different columns you can specify them in a dict
# my_missing_2 = {'cut':'-1','clarity':'NaN','price':['NULL','-999'],'y':'NaN'}
# dia_5a = pd.read_csv(path+'diamonds_4.csv',na_values=my_missing_2)
# # Interestingly this didn't work for the cut variable. Any idea why?
#
# ################################################################################
#
# # Writing data out to csv files with .to_csv method for Series/DataFrames
# my_series = Series({'a':np.arange(10)})
# my_series.to_csv(path+'my_series.csv',header=True)
# # Same with data frames
# my_df = DataFrame({'a':np.arange(5),'b':np.arange(5,10),'c':np.arange(10,15)})
# my_df.to_csv(path+'my_df.csv')
#
# # Other arguments to to_csv
# my_series.to_csv(path+'my_series_2.csv',sep='\t',header=True)
#
# # If there are missing values in your data, decide what to do with them
# my_series_3 = Series([1,2,3,None,4])
# my_series_3.to_csv(path+'my_series_3.csv',header=False) # By default will leave it blank
# my_series_3.to_csv(path+'my_series_4.csv',na_rep='NA',header=False) # turns it into NA
#
# # index, header, cols and rows arguments to .to_csv
# # Turn off the row index names with index=False, col index with header
# my_df.to_csv(path+'my_df_2.csv',index=False, header=False)
# # Choose which columns to write out with columns
# my_df.to_csv(path+'my_df_3.csv',columns='a')

# Reading and writing other types of data

# Json data
# Other read functions
# clipboard, excel, hdf, fwf, html, sql, stata

# Other to functions
# to_dict, to_latex, to_excel, to_clipboard, to_html

# More in this chapter on web scraping and APIs but we'll cover this later

################################################################################

# Now on to Data Wrangling - chapter 7 of McKinney

# Example from book: movie lens data
# Three data sets, first the list of movies
# movies = pd.read_csv('ml-1m/movies.dat',sep='::',names=['movie_id','title','genres'],engine='python')
# Second the list of ratings (this is big so use the nrows argument if it's slowing you down)
ratings = pd.read_csv('ml-1m/ratings.dat',sep='::',names=['user_id','movie_id','rating','timestamp'],engine='python')
# List of users
# users = pd.read_csv('ml-1m/users.dat',sep='::',names=['user_id','gender','age','occupation','zip'],engine='python')
# Note engine arguement, default engine ('c') doesn't support separators ('::') of more than one character

# First pd.merge - suppose we want to link together the details about the users and the ratings
# Note that the ratings DataFrame has lots of rows with the same users, see e.g.
# ratings.head()

# So we now want each row to contain their rating and all their details
# ratings_and_users = pd.merge(ratings,users) # notice how quick this is!
# ratings_and_users.head(10)

# on, left_on, right_on arguments for merge
# Can specify the key on which to merge, but merge will automatically work this out if required
# ratings_and_users = pd.merge(ratings,users,on='user_id')

# # Notice that if I'd put in the column index differently I can specify the indices to match on for each data set
# users_2 = pd.read_csv('ml-1m/users.dat',sep='::',engine='python',names=['userid','gender','age','occupation','zip'])
# ratings_and_users2 = pd.merge(ratings,users_2,left_on='user_id',right_on='userid')
#
# # What if I had merged these the other way round?
# other_merge = pd.merge(users,ratings,on='user_id')
# # Works without error - does the same thing but puts the columns in a slightly different order
#
# # Multiple keys
# # If you a have multiple keys to match on, specify them as a list in the on argument
#
# # Using the index as the merge key with left_index and right_index
# # Sometimes you want to merge based on the indices
# # Let's loas the data in using the 'user_id' column as the index
# ratings_3 = pd.read_csv('ml-1m/ratings.dat',sep='::',engine='python',names=['user_id','movie_id','rating','timestamp'],index_col='user_id')
# users_3 = pd.read_csv('ml-1m/users.dat',sep='::',engine='python',names=['user_id','gender','age','occupation','zip'],index_col='user_id')
# # Can specify this explicitly in the merge
# ratings_and_users_3 = pd.merge(ratings_3,users_3,left_index=True,right_index=True)
#
# ## Concatenating data frames
#
# # Back to the iphone/galaxy DataFrames
iphone_dict = {'Name': ['iPhone', 'iPhone 3G', 'iPhone 3GS', 'iPhone 4', 'iPhone 4S', 'iPhone 5', 'iPhone 5C', 'iPhone 5S'],
    'Memory_MB': [128, 128, 256, 512, 512, 1024, 1024, 1024],
    'Weight_g': [135, 133, 135, 137, 140, 112, 132, 112],
    'Camera_MP': [2, 2, 3, 5, 8, 8, 8, 8],
    'Year': [2007, 2008, 2009, 2010, 2011, 2012, 2013, 2013] }
iphone_df = DataFrame(iphone_dict,index=iphone_dict['Year'])
galaxy_dict = {'Name': ['Galaxy S', 'Galaxy S II', 'Galaxy S III', 'Galaxy S 4', 'Galaxy S 5'],
    'Memory_MB': [512, 1024, 1024, 2048, 2048],
    'Weight_g': [119, 116, 133, 130, 145],
    'Camera_MP': [5, 8, 8, 13, 16],
    'Year': [2010, 2011, 2012, 2013, 2014] }
galaxy_df = DataFrame(galaxy_dict,index=galaxy_dict['Year'])

# # Suppose we want to join these two together? How might we want to join them?
#
# # First consider stacking them on top of each other using concatenate
pd.concat([iphone_df,galaxy_df],sort=False)
# # What happens when the columns don't match exactly?
pd.concat([iphone_df.drop('Camera_MP',axis=1),galaxy_df],sort=False)
# # Can give it more than two objects
pd.concat([iphone_df,galaxy_df,iphone_df],sort=False)
# # Note: sort=True will sort the output columns in alphabetical order
#
# # What if instead we wanted it joined by year? Could use join
iphone_df.join(galaxy_df,lsuffix='Apple')
# # Or you could go back to merge
pd.merge(iphone_df,galaxy_df,on='Year')
# # Note the how='outer' means it doesn't throw away any rows where things don't match
#
# # Another useful function for combining DataFrames is combine_first:
iphone_df.combine_first(galaxy_df)
galaxy_df.combine_first(iphone_df)
# # Can you see what it is doing? It's merging the indices and then filling in the
# # missing values from the other DataFrame - neat!
#
# ################################################################################
#
# # Removing duplicates with .duplicated() and drop_duplicates()
#
# # Let's play around again with the users movie lens function
#
# # First re-load the data in case you've lost it
# ratings = pd.read_csv(path + 'ml-1m/ratings.dat',sep='::',engine='python',names=['user_id','movie_id','rating','timestamp'])
#
# # Let's find out how many user IDs are duplicated, i.e. have multiple reviews
ratings.user_id.duplicated()
# # A bit long
ratings.user_id.duplicated().sum() # 994,169!
#
# # Drop the duplicates
# ratings.user_id.drop_duplicates() # Lenght 6040
# # An alternative to this that is perhaps neater is:
# ratings.drop_duplicates('user_id')
#
# # Mapping data
# # Let's have a look at the users data again, specifically the age column
users = pd.read_csv(path + 'ml-1m/users.dat',sep='::',engine='python',names=['user_id','gender','age','occupation','zip'])
# users.age.value_counts()
# # The README file in the movie lens folder says that these correspond to:
# #  1:  "Under 18"
# # 18:  "18-24"
# # 25:  "25-34"
# # 35:  "35-44"
# # 45:  "45-49"
# # 50:  "50-55"
# # 56:  "56+"
#
# # Let's create a mapping dict:
# my_map = {1:'Under 18',18:'18-24',25:'25-34',35:'35-44',45:'45-49',50:'50-55',56:'56+'}
# users['age_grp'] = users['age'].map(my_map)
# users.head()
#
# # You can also use a lambda function
# users['age_grp_2'] = users['age'].map(lambda x: my_map[x])
#
# # Yet another alternative for doing this in place is replace
# users['age'] = users['age'].replace([1,18,25,35,45,50,56],['Under 18','18-24','25-34','35-44','45-49','50-55','56+'])
#
# # The cut method
# # Let's suppose we had raw ages rather than age groups above and wanted to group
# # them in the same way
# ages = Series(npr.poisson(lam=40,size=100))
# bins = [0,20,40,60]
# age_groups = pd.cut(ages,bins)
#
# # For some reason this is a special type of Categorical object
# type(age_groups)
# pd.value_counts(age_groups)
#
# # You can even give these labels:
# age_groups = pd.cut(ages,bins,labels=['Young','Middle-aged','Old'])
# pd.value_counts(age_groups)
#
# # Or you can give cut just a number of bins
# pd.cut(ages,4,precision=0)
# # Or use qcut which cuts by quantiles
# pd.qcut(ages,4) # quartiles
# # You can give qcut your own quantiles
# pd.qcut(ages,[0.,0.25,0.5,0.75,1.])
#
# # To finish off - a useful little trick the get_dummies method for
# # creating indicator variables (i.e. 0s and 1s) categorical variables
# # This is widely used in regression and classification
#
# # Suppose we wanted to turn the rating column in the ratings DataFrame
# # into indicator variables:
# pd.get_dummies(ratings['rating'])
# # Combining get dummies with cut can also be useful
#
# ################################################################################
#
