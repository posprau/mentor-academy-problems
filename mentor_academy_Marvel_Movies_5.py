# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 17:54:10 2017

@author: Peter Sprau
"""

## SETUP 

import pandas as pd
import numpy as np
proxy='https://proxy.mentoracademy.org/getContentFromWikiUrl/'
wikipage = 'https://en.wikipedia.org/wiki/List_of_films_based_on_Marvel_Comics'
tables = pd.read_html(wikipage)

# load table about budget and box office for Marvel Movies

## box office
# =============================================================================
df1 = tables[9]
df1 = df1.iloc[2:-2,:]
# reset the index of the dataframe
df1 = df1.reset_index(drop=True)
# indices of defect rows that need to be shifted right by one, and miss value
# for distributor due to structure of table on wikipedia
defRows = [6,13,15,22,31,35,36,37,39]

for i in defRows:
    # shift row right by one
    df1.iloc[i,1:] = df1.iloc[i,1:].shift(1,axis=0)
    # distributor is same as from row before
    df1.iloc[i,1] = df1.iloc[i-1,1]
# drop columns about box office opening weekend, and split of box office results
# into North America and other territories, only keep box office world wide
df1 = df1.drop([4,5,6],axis=1)
# rename the columns
df1 = df1.rename( columns={0:'Title', 1:'Distributor',\
            2:'Release Date', 3:'Budget ($)', 7:'Box Office World ($)'} )
    
# convert column for box office into floats
df1.loc[:46,'Box Office World ($)'] = df1.loc[:46,'Box Office World ($)'].\
apply( lambda x: x.split('$')[1] )

df1.loc[:46,'Box Office World ($)'] = df1.loc[:46,'Box Office World ($)'].\
apply( lambda x: ''.join( x.split(',') ) )

df1['Box Office World ($)'] = df1['Box Office World ($)'].apply( pd.to_numeric )

# convert column for budget into floats
df1.loc[:45,'Budget ($)'] = df1.loc[:45,'Budget ($)'].\
apply( lambda x: x.split('$')[1] )
df1.loc[47,'Budget ($)'] = df1.loc[47,'Budget ($)'].split('$')[1]

df1['Budget ($)'] = df1['Budget ($)'].apply( pd.to_numeric ) * 10**6

# rename latest Fantastic Four reboot
df1.loc[38,'Title'] = 'Fantastic Four (2015)'

df1

# =============================================================================
# =============================================================================
# =============================================================================

## QUESTION 
# Iron Man has been a very successful franchise for Marvel. You  
# want to know how much time has passed between the individual 
# Iron Man movies, and how much time has passed since the last 
# Iron Man movie ('Iron Man 3') with respect to today's date? 
# 
# The expected output is a tuple of three numbers with one decimal
# point, e.g. (1.0, 3.5, 0.8). The first number is the approximate
# number of years between 'Iron Man' and 'Iron Man 2', the second
# number the same for 'Iron Man 2' and 'Iron Man 3', and the last 
# the same for 'Iron Man 3' and today's date.

# Hint 1: Changing the index of the dataframe from numbers to movie
# titles will allow you to directly access the 'Release Date' of a 
# specific movie by its title.

# Hint 2: pd.to_datetime('January 1, 2000') returns a Timestamp.
# The difference between two Timestamps is a Timedelta.

# Hint 3: Timedelta.days returns the number of days in the 
# Timedelta. If you divide this number by 365 you will get the 
# approximate number of years.

# Hint 4: pd.to_datetime('today') returns the Timestamp for
# today's date.

# Hint 5: float('{0:.1f}'.format(x)) will return x with one decimal place.

## SOLUTION
def solution():
    boxO = df1 # box office dataframe from setup
    
    # convert the release date column from strings to timestamps
    boxO['Release Date'] = pd.to_datetime(boxO['Release Date'])
    
    # create new dataframe where index of dataframe is based on the movie title 
    # column
    indexed_df = boxO.set_index(['Title'])
    
    # compute timedelta between Iron Man movies
    delta1 = indexed_df.loc['Iron Man 2','Release Date'] - \
    indexed_df.loc['Iron Man','Release Date']
    delta2 = indexed_df.loc['Iron Man 3','Release Date'] - \
    indexed_df.loc['Iron Man 2','Release Date']
    
    # get today's date and compute timedelta between Iron Man 3 and today
    todayDate = pd.to_datetime('today')
    delta3 = todayDate - indexed_df.loc['Iron Man 3','Release Date']

    # convert timedelta into approximate number of years with one decimal place
    # precision
    ans1 = float('{0:.1f}'.format(delta1.days / 365))
    ans2 = float('{0:.1f}'.format(delta2.days / 365))
    ans3 = float('{0:.1f}'.format(delta3.days / 365))
    
    return  ans1, ans2, ans3 