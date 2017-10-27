# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 17:41:43 2017

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

# load table with review scores from Rotten Tomatoes for Marvel Movies

## critical Success
# =============================================================================
df2 = tables[10][[0,1]]
df2 = df2.iloc[1:-1,:]
df2 = df2.reset_index(drop=True)
# correct two review score entries
df2.loc[2,1] = '8%'
df2.loc[42,1] = '9%'
# convert review score column into floats
df2 = df2.rename( columns={0:'Title', 1:'Review Score (%)'} )
df2['Review Score (%)'] = df2['Review Score (%)'].apply( lambda x: x.split('%')[0] )
df2['Review Score (%)'] = df2['Review Score (%)'].apply( pd.to_numeric)
# delete (year) for some of the movies, but not latest Fantastic Four reboot
# and first Punisher movie
df2['Title'] = df2['Title'].apply( lambda x: x.split(' (')[0] )
df2.loc[42,'Title'] = 'Fantastic Four (2015)'
df2.loc[1,'Title'] = 'The Punisher (1989)'

df2

# =============================================================================
# =============================================================================
# =============================================================================

## QUESTION 
# Use the movie title to merge the two dataframes so 
# that the results for box office and review scores
# are combined within one dataframe.

## SOLUTION
def solution():
    boxO = df1 # box office dataframe from setup
    critS = df2 # critical success dataframe from setup
    
    # merge dataframes on 'Title' column of the movies
    df3 = boxO.merge(critS, how='inner', on='Title')
    return df3