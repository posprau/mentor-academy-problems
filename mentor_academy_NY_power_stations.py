# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 17:26:09 2017

@author: Peter Sprau
"""

import pandas as pd
import numpy as np
proxy='https://proxy.mentoracademy.org/getContentFromWikiUrl/'
wikipage = 'https://en.wikipedia.org/wiki/List_of_power_stations_in_New_York'
tables = pd.read_html(proxy+wikipage)

# load tables for coal, gas, petroleum, nuclear, hydroelectric, windfarms,
# and biomass power plants, and turn into dataframes with columns for name of
# the plant, its location, and its output in MW.

## coal
# =============================================================================
df = tables[0][[0,1,3]]
coal = df.iloc[1:,:]
coal = coal.rename( columns = {0:'Plant', 1:'Location', 3:'Output (MW)'} )
coal['Plant'] = coal['Plant'].apply( lambda x: x.split('[')[0] )
coal['Output (MW)'] = coal['Output (MW)'].apply( pd.to_numeric )
# =============================================================================

## gas
# =============================================================================
df = tables[2][[0,1,3]]
gas = df.iloc[1:,:]
gas = gas.rename( columns = {0:'Plant', 1:'Location', 3:'Output (MW)'} )
gas['Plant'] = gas['Plant'].apply( lambda x: x.split('[')[0] )
gas['Output (MW)'] = gas['Output (MW)'].apply( pd.to_numeric )
# =============================================================================

## petroleum
# =============================================================================
df = tables[3][[0,1,3]]
petroleum = df.iloc[1:,:]
petroleum = petroleum.rename( columns = {0:'Plant', 1:'Location', 3:'Output (MW)'} )
petroleum['Plant'] = petroleum['Plant'].apply( lambda x: x.split('[')[0] )
petroleum['Output (MW)'] = petroleum['Output (MW)'].apply( pd.to_numeric )
# =============================================================================

## nuclear
# =============================================================================
df = tables[1][[0,1,3]]
nuclear = df.iloc[1:,:]
nuclear = nuclear.rename( columns = {0:'Plant', 1:'Location', 3:'Output (MW)'} )
nuclear['Plant'] = nuclear['Plant'].apply( lambda x: x.split('[')[0] )
nuclear['Output (MW)'] = nuclear['Output (MW)'].apply( pd.to_numeric )
# =============================================================================

## hydroelectric
# =============================================================================
df = tables[4][[0,1,3]]
hydro = df.iloc[1:,:]
hydro = hydro.rename( columns = {0:'Plant', 1:'Location', 3:'Output (MW)'} )
hydro['Plant'] = hydro['Plant'].apply( lambda x: x.split('[')[0] )
hydro['Output (MW)'] = hydro['Output (MW)'].apply( pd.to_numeric )
# =============================================================================

## wind farms
# =============================================================================
df = tables[5][[0,1,3]]
wind = df.iloc[1:,:]
wind = wind.rename( columns = {0:'Plant', 1:'Location', 3:'Output (MW)'} )
wind['Plant'] = wind['Plant'].apply( lambda x: x.split('[')[0] )
wind['Output (MW)'] = wind['Output (MW)'].apply( pd.to_numeric )
# =============================================================================

## biomass
# =============================================================================
df = tables[6][[0,1,3]]
biomass = df.iloc[1:,:]
biomass = biomass.rename( columns = {0:'Plant', 1:'Location', 3:'Output (MW)'} )
biomass['Plant'] = biomass['Plant'].apply( lambda x: x.split('[')[0] )
biomass['Output (MW)'] = biomass['Output (MW)'].apply( pd.to_numeric )
# =============================================================================

# display dataframe for gas power stations as example
nuclear

# =============================================================================
# =============================================================================
# =============================================================================

## QUESTION 1
# Sort the dataframe in descending order of Output in MW generated by the 
# nuclear power stations, and reset the index of the dataframe afterwards.

# Solution
def solution1(nuclear):
    # sort the dataframe in descending order of Output in MW generated by power 
    # plant
    nuclear = nuclear.sort_values('Output (MW)', ascending = False)
    # reset the index of the dataframe
    nuclear = nuclear.reset_index(drop=True) 
    return nuclear

## QUESTION 2
# Combine the dataframes for hydroelectric, wind farms, and biomass power 
# stations into a single dataframe. Sort the dataframe in descending order of 
# Output in MW generated by the renewable power stations, 
# and reset the index of the dataframe afterwards.

# Solution
def solution2(hydro, wind, biomass):
    # combine the hydroelectric, wind farms and biomass power stations
    renewable = hydro.append([wind,biomass])
    # sort the dataframe in descending order of Output in MW generated by power
    # plant
    renewable = renewable.sort_values('Output (MW)', ascending = False)
    # reset the index of the dataframe
    renewable = renewable.reset_index(drop=True)
    return renewable

## QUESTION 3
# Combine the dataframes for coal, gas, and petroleum power stations into a 
# single dataframe. Some power stations appear both in the list for gas and 
# petroleum power stations, so these duplicate entries need to be deleted. 
# Sort the dataframe in descending order of Output in MW generated by the 
# fossil fuel power stations, and reset the index of the dataframe afterwards.

# Solution
def solution3(gas, petroleum, coal):
    # combine the gas and petroleum dataframes using the append method
    oilGas = gas.append(petroleum)
    # drop all duplicates
    oilGas = oilGas.drop_duplicates()
    # add the coal power plants
    fossilFuel = oilGas.append(coal)
    # sort the dataframe in descending order of Output in MW generated by plant
    fossilFuel = fossilFuel.sort_values('Output (MW)', ascending = False)
    # reset the index of the dataframe
    fossilFuel = fossilFuel.reset_index(drop=True)
    return fossilFuel

## QUESTION 4
# Compute and return a tuple with the percentages of renewable, nuclear, and 
# fossil fuel power generated in New York state with respect to the total 
# power generated by all three type of sources. Each percentage should be a 
# float with four decimal places. For example, if 12.57 % renewable, 35.29 % 
# nuclear, and 52.14 % fossil fuel power was generated the output should
# be (0.1257, 0.3529, 0.5214).

# Solution
nuclear = solution1(nuclear)
renewable = solution2(hydro, wind, biomass)
fossilFuel = solution3(gas, petroleum, coal)

def solution4(nuclear, renewable, fossilFuel):
    # compute the total output of all forms of energy sources (nuclear, fossil
    # fuel, and renewable)
    renOut = sum(renewable['Output (MW)'])
    nucOut = sum(nuclear['Output (MW)'])
    fosOut = sum(fossilFuel['Output (MW)'])
    totalOut = renOut + nucOut + fosOut
             
    # return a tuple with the percentages of renewable, nuclear, and fossil fuel
    # as floats with four decimal places
    renOutPC = float('{0:.4f}'.format(renOut/totalOut)) 
    nucOutPC = float('{0:.4f}'.format(nucOut/totalOut))
    fosOutPC = float('{0:.4f}'.format(fosOut/totalOut))
    
    result = (renOutPC, nucOutPC, fosOutPC)
    return result