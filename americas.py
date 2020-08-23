#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This will be the helper file that will contain the functions for 
1) StatesList
2) HeadlinesPerState
"""

import numpy as np
import pandas as pd
import requests
import json
from helpers import ListOfDates

def StatesList():
    """
    Returns a list of all US states on which the Johns Hopkins API has information
    """

    # Contact Johns Hopkins API
    try:
        response = requests.get(f"https://disease.sh/v3/covid-19/historical/usacounties")
        response.raise_for_status()
    except requests.RequestException:
        return None

    return response.json()

def ConvertWMtoJH(input, state):
    """
    Converts the state name as used in the WorldoMeter API to the state name used in the John Hopkins API or the other way around
    If input is 'JH' the function will transform a JH state into a WM state
    If input is 'WM' the function will transform a WM state into a JH state
    In case of any other input or a key error the function will return None
    """

    from_JHtoWM = {'alabama': 'Alabama','alaska': 'Alaska','arizona': 'Arizona','arkansas': 'Arkansas', 
    'california': 'California', 'colorado': 'Colorado', 'connecticut': 'Connecticut','delaware': 'Delaware', 'diamond princess': 'Diamond Princess Ship', 
    'district of columbia': 'District Of Columbia', 'florida': 'Florida', 'georgia': 'Georgia', 'grand princess': 'Grand Princess Ship', 'guam': 'Guam', 
    'hawaii': 'Hawaii', 'idaho': 'Idaho', 'illinois': 'Illinois', 'indiana': 'Indiana', 'iowa': 'Iowa', 'kansas': 'Kansas', 'kentucky': 'Kentucky', 
    'louisiana': 'Louisiana', 'maine': 'Maine', 'maryland': 'Maryland', 'massachusetts': 'Massachusetts', 'michigan': 'Michigan', 
    'minnesota': 'Minnesota', 'mississippi': 'Mississippi', 'missouri': 'Missouri', 'montana': 'Montana', 'nebraska': 'Nebraska', 'nevada': 'Nevada', 
    'new hampshire': 'New Hampshire', 'new jersey': 'New Jersey', 'new mexico': 'New Mexico', 'new york': 'New York', 'north carolina': 'North Carolina', 
    'north dakota': 'North Dakota', 'northern mariana islands': 'Northern Mariana Islands', 'ohio': 'Ohio', 'oklahoma': 'Oklahoma', 'oregon': 'Oregon', 
    'pennsylvania': 'Pennsylvania', 'puerto rico': 'Puerto Rico', 'rhode island': 'Rhode Island', 'south carolina': 'South Carolina', 
    'south dakota': 'South Dakota', 'tennessee': 'Tennessee', 'texas': 'Texas', 'utah': 'Utah', 'vermont': 'Vermont', 'virgin islands': 'United States Virgin Islands', 
    'virginia': 'Virginia', 'washington': 'Washington', 'west virginia': 'West Virginia', 'wisconsin': 'Wisconsin', 'wyoming': 'Wyoming'}

    output = None

    if input == 'JH':
        try:
            output = from_JHtoWM[state]
        except KeyError:
            output = None
    
    if input == 'WM':
        from_WMtoJH = {v: k for k, v in from_JHtoWM.items()}
        try:
            output = from_WMtoJH[state]
        except KeyError:
            output = None

    return output


def HeadlinesPerStateWM(state):
    """
    Look up headline statistics per US state starting as of 1 Jan 2020. Function returns a dict with 
    {'state':, 'updated':, 'cases':, 'todayCases':, 'deaths':, 'todayDeaths':, 'active':, 
    'casesPerOneMillion':, 'deathsPerOneMillion':, 'tests':, 'testsPerOneMillion':}

    This uses the API from Worldometer, which uses different state names than the Johns Hopkins API
    """

    # Contact the Woldometer API
    try:
        response = requests.get(f"https://disease.sh/v3/covid-19/states/{state}/")
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        stateStats = response.json()
        return {
            "name": stateStats["state"],
            "cases": stateStats["cases"],
            "todayCases": stateStats["todayCases"],
            "deaths": stateStats["deaths"],
            "todayDeaths": stateStats["todayDeaths"],
            "active": stateStats["active"],
            "tests": stateStats["tests"],
            "casesPerOneMillion": stateStats["casesPerOneMillion"],
            "deathsPerOneMillion": stateStats["deathsPerOneMillion"],
            "testsPerOneMillion": stateStats["testsPerOneMillion"]
            }
    except (KeyError, TypeError, ValueError):
        return None

def InhabitantsPerState(state):
    """
    Returns the number of inhabitants per state as based on the Census count of July 2019.
    This includes the diamond princes and grand princes, wihch are two ships 
    """
    stateInhabitants = {'alabama': 4903185,'alaska': 731545,'american samoa': 49437,'arizona': 7278717,'arkansas': 3017804, 
    'california': 39512223, 'colorado': 5758736, 'connecticut': 3565287,'delaware': 973764, 'diamond princess': 3711, 
    'district of columbia': 705749, 'florida': 21477737, 'georgia': 10617423, 'grand princess': 3711, 'guam': 168485, 
    'hawaii': 1415872, 'idaho': 1787065, 'illinois': 12671821, 'indiana': 6732219, 'iowa': 3155070, 'kansas': 2913314, 'kentucky': 4467673, 
    'louisiana': 4648794, 'maine': 1344212, 'maryland': 6045680, 'massachusetts': 6892503, 'michigan': 9986857, 
    'minnesota': 5639632, 'mississippi': 2976149, 'missouri': 6137428, 'montana': 1068778, 'nebraska': 1934408, 'nevada': 3080156, 
    'new hampshire': 1359711, 'new jersey': 8882190, 'new mexico': 2096829, 'new york': 19453561, 'north carolina': 10488084, 
    'north dakota': 762062, 'northern mariana islands': 51433, 'ohio': 11689100, 'oklahoma': 3956971, 'oregon': 4217737, 
    'pennsylvania': 12801989, 'puerto rico': 3193694, 'rhode island': 1059361, 'south carolina': 5148714, 
    'south dakota': 884659, 'tennessee': 6829174, 'texas': 28995881, 'utah': 3205958, 'vermont': 623989, 'virgin islands': 106235, 
    'virginia': 8535519, 'washington': 7614893, 'west virginia': 1792147, 'wisconsin': 5822434, 'wyoming': 578759}

    return stateInhabitants[state]

def HistPerState(state):
    """
    Look up historical statistics per US state. Function returns a dict with 
    {"name":"california","history":{
    "cases":{"1/22/20":0,"1/23/20":0},
    "deaths":{"1/22/20":0,"1/23/20":0},
    }}
    start date is alway 1/1/20   
    """
 
    # Contact Johns Hopkins API
    try:
        response = requests.get(f"https://disease.sh/v3/covid-19/historical/usacounties/{state}?lastdays=all")
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Create a JSON object containing the historical stats for all counties in the state
    try:
        stateStats = response.json()
    except (KeyError, TypeError, ValueError):
        return None

    # Initialise the required support variables
    datesList = ListOfDates(stateStats[0]['timeline']['cases'])
    dictCases = {}
    dictDeaths = {}
    numCounties = len(stateStats)

    # For each date in the list add up all the cases and all the deaths per county and parse these into two new dicts
    for date in datesList:
        cases = 0
        deaths = 0
        for i in range(numCounties):
            try:
                cases = cases + stateStats[i]['timeline']['cases'][date]
                deaths = deaths + stateStats[i]['timeline']['deaths'][date]
            except KeyError:
                None
        dictCases[date]=cases
        dictDeaths[date]=deaths
    
    # Create the final dict and return it
    timelineDict = {}
    timelineDict["cases"] = dictCases
    timelineDict["deaths"] = dictDeaths
    histDict = {}
    histDict["name"] = stateStats[0]["province"]
    histDict["history"] = timelineDict
    return histDict

def HistPerStateLong(state):
    """
    Look up historical statistics per US state. Function returns a dict with 
    {"name":"california","history":{
    "cases":{"1/1/20":0,"1/2/20":0},
    "newCases":{"1/1/20":0,"1/2/20":0},
    "casesPerOneMLN":{"1/1/20":0,"1/2/20":0}, 
    "deaths":{"1/1/20":0,"1/2/20":0},
    "newDeaths":{"1/1/20":0,"1/2/20":0},
    "deathsPerOneMLN":{"1/1/20":0,"1/2/20":0},
    }}   
    """

    # load the basics and define the denominator (x million inhabitants)
    basics = HistPerState(state)
    dates = ListOfDates(basics['history']['cases'])
    newDict = {}
    newDict['name'] = basics['name']

    # create dictionaries for historical cases, new cases and number of cases per 1MLN 
    casesT={}
    newCases={}
    casesPerOneMillion={}
    denom = InhabitantsPerState(state)
    currentCases = 0

    for i in dates:
        try:
            myValue = basics['history']['cases'][i]
            casesT[i] = myValue
            newCases[i] = max(myValue - currentCases,0)
            casesPerOneMillion[i] = round(myValue/denom,0)
            currentCases = myValue
        except(KeyError):
            casesT[i] = 0
            newCases[i] = 0
            casesPerOneMillion[i] = 0

    # create dictionaries for historical deaths, new deaths and number of deaths per 1MLN 
    deathsT={}
    newDeaths={}
    deathsPerOneMillion={}
    currentDeaths = 0

    for i in dates:
        try:
            myValue = basics['history']['deaths'][i]
            deathsT[i] = myValue
            newDeaths[i] = max(myValue - currentDeaths,0)
            deathsPerOneMillion[i] = round(myValue/denom,0)
            currentDeaths = myValue
        except(KeyError):
            deathsT[i] = 0
            newDeaths[i] = 0
            deathsPerOneMillion[i] = 0

    # patch all the dictionaries to eachother and add them to the main dict

    history={}
    history['cases'] = casesT
    history['newCases'] = newCases
    history['casesPerOneMLN'] = casesPerOneMillion
    history['deaths'] = deathsT
    history['newDeaths'] = newDeaths
    history['deathsPerOneMLN'] = deathsPerOneMillion
    newDict['history'] = history
    
    return newDict


if __name__ == "__main__":

    stateName = ConvertWMtoJH('bl', 'california')
    print(stateName)

    
    




    

