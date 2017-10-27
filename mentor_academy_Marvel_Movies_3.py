# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 17:49:09 2017

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
# How profitable have Marvel movies been with different distributors? 
# Return a dataframe with 8 rows, and 3 columns:
# The row indices are the values of the Distributor column ( 20th Century
# Fox, New Line Cinema, ...). The three columns are given by the aggregated 
# sum of 'Budget ($)' and 'Box Office World ($)' columns, and a new column
# called the 'Profit in Million $' which has to be created using the aggregated
# values for each distributor.

# Assume that the profit is the difference of the box office value and 
# budget value, and don't forget to divide the profit by 10^6.

## SOLUTION
def solution():
    boxO = df1 # box office dataframe from setup
    
    # group by Distributor and sum over budget and box office column
    df = boxO.groupby(['Distributor'])['Budget ($)','Box Office World ($)'].sum()
    # add a column for the profit:= box office - budget
    df['Profit in Million $'] = (df['Box Office World ($)'] - \
                                 df['Budget ($)'])/(10**6)
    
    return df