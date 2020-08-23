#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This will be the helper file that will contain the functions for 
1) HistPerCountry
2) HistPerCountryLong
3) HeadlinesPerCountry
4) CountryList
5) ConvertToList
6) ListOfDates
7) TopList
8) ColorList
9) KPIList
10) SinceDayX
11) WeeklyDeathsPerCountry
12) TotalDeathsEU
"""

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime
import json
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError

def HistPerCountry(country):
    """
    Look up historical statistics per country. Function returns a dict with 
    {"standardizedCountryName":"netherlands","history":{
    "cases":{"1/22/20":0,"1/23/20":0},
    "deaths":{"1/22/20":0,"1/23/20":0},
    "recovered":{"1/22/20":0,"1/23/20":0}
    }}
    start date varies per country   
    """
 
    # Contact API
    try:
        response = requests.get(f"https://corona.lmao.ninja/v2/historical/{country}?lastdays=all")
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        countryStats = response.json()
        return {
            "name": countryStats["country"],
            "history": countryStats["timeline"],
        }
    except (KeyError, TypeError, ValueError):
        return None

def HistPerCountryLong(country):
    """
    Look up historical statistics per country. Function returns a dict with 
    {"standardizedCountryName":"netherlands","history":{
    "cases":{"1/1/20":0,"1/2/20":0},
    "newCases":{"1/1/20":0,"1/2/20":0},
    "casesPerOneMLN":{"1/1/20":0,"1/2/20":0}, 
    "deaths":{"1/1/20":0,"1/2/20":0},
    "newDeaths":{"1/1/20":0,"1/2/20":0},
    "deathsPerOneMLN":{"1/1/20":0,"1/2/20":0},
    "recovered":{"1/1/20":0,"1/2/20":0},
    "newRecovered":{"1/1/20":0,"1/2/20":0},
    "recoveredPerOneMLN":{"1/1/20":0,"1/2/20":0},
    }}   
    """

    # load the basics and define the denominator (x million inhabitants)
    basics = HistPerCountry(country)
    dates = ListOfDates(basics['history']['cases'])
    newDict = {}
    newDict['name'] = basics['name']
    
    headlines = HeadlinesPerCountry(country)
    try:
        denom = headlines['cases']/headlines['casesPerOneMillion']
    except ZeroDivisionError:
        denom = 1

    # create dictionaries for historical cases, new cases and number of cases per 1MLN 
    casesT={}
    newCases={}
    casesPerOneMillion={}
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

    # create dictionaries for historical recoveries, new recoveries and number of recoveries per 1MLN 
    recoveredT={}
    newRecovered={}
    recoveredPerOneMillion={}
    currentRecovered = 0

    for i in dates:
        try:
            myValue = basics['history']['recovered'][i]
            recoveredT[i] = myValue
            newRecovered[i] = max(myValue - currentRecovered,0)
            recoveredPerOneMillion[i] = round(myValue/denom,0)
            currentRecovered = myValue
        except(KeyError):
            recoveredT[i] = 0
            newRecovered[i] = 0
            recoveredPerOneMillion[i] = 0

    # patch all the dictionaries to eachother and add them to the main dict

    history={}
    history['cases'] = casesT
    history['newCases'] = newCases
    history['casesPerOneMLN'] = casesPerOneMillion
    history['deaths'] = deathsT
    history['newDeaths'] = newDeaths
    history['deathsPerOneMLN'] = deathsPerOneMillion
    history['recovered'] = recoveredT
    history['newRecovered'] = newRecovered
    history['recoveredPerOneMLN'] = recoveredPerOneMillion
    newDict['history'] = history
    
    return newDict

def HeadlinesPerCountry(country):
    """
    Look up headline statistics per country starting as of 1 Jan 2020. Function returns a dict with 
    {"name":,
    "countryInfo":{}
    "cases":,"todayCases":,"deaths":,"todayDeaths":,"recovered":,"active":,"critical":,
    "casesPerOneMillion":,deathsPerOneMillion"}   
    """

    # Contact API
    try:
        response = requests.get(f"https://corona.lmao.ninja/v2/countries/{country}/")
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        countryStats = response.json()
        return {
            "name": countryStats["country"],
            "countryInfo": countryStats["countryInfo"],
            "cases": countryStats["cases"],
            "todayCases": countryStats["todayCases"],
            "deaths": countryStats["deaths"],
            "todayDeaths": countryStats["todayDeaths"],
            "recovered": countryStats["recovered"],
            "active": countryStats["active"],
            "critical": countryStats["critical"],
            "casesPerOneMillion": countryStats["casesPerOneMillion"],
            "deathsPerOneMillion": countryStats["deathsPerOneMillion"],
            "testsPerOneMillion": countryStats["testsPerOneMillion"]
            }
    except (KeyError, TypeError, ValueError):
        return None

def CountryList():
    """
    Returns a list of all countries on which the API has information
    """

    # Contact API
    try:
        response = requests.get("https://corona.lmao.ninja/v2/countries")
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        countryStats = response.json()
        countryNames = []
        for i in range(len(countryStats)):
            countryNames.append(countryStats[i]["country"])
        countryNames.sort()
        return countryNames
    except (KeyError, TypeError, ValueError):
        return None

def ConvertToList(dictInput):
    """
    Converts a dictionary with dates as key into a list with data points starting from 1/1/2020
    """

    # initialise the set. We start from 1 Jan 2020 and continue till today
    currentDate = datetime.date(2020, 1, 1)
    one_day = datetime.timedelta(days=1)
    dateList = []
    numberDays = datetime.date.today() - currentDate
    numberDays = numberDays.days

    # the API uses a specific string format ('m/d/yy') as keys to the dicionary
    dateString = str(currentDate.month)+"/"+str(currentDate.day)+"/"+str(currentDate.strftime("%y"))
    
    # fill the list with data points. If a date does not exist, replace the number with zero
    for i in range(numberDays):
        try:
            number = dictInput[dateString]
        except (KeyError):
            number = 0
        dateList.append(number)
        currentDate = currentDate + one_day
        dateString = str(currentDate.month)+"/"+str(currentDate.day)+"/"+str(currentDate.strftime("%y"))
    
    return dateList

def ListOfDates(dictInput):
    """
    Converts a dictionary with dates as key into a list with dates starting from 1/1/2020
    """

    # initialise the set. We start from 1 Jan 2020 and continue till today
    currentDate = datetime.date(2020, 1, 1)
    one_day = datetime.timedelta(days=1)
    dateList = []
    numberDays = datetime.date.today() - currentDate
    numberDays = numberDays.days

    # the API uses a specific string format ('m/d/yy') as keys to the dicionary
    dateString = str(currentDate.month)+"/"+str(currentDate.day)+"/"+str(currentDate.strftime("%y"))
    
    # fill the list with data points. If a date does not exist, replace the number with zero
    for i in range(numberDays):
        dateList.append(dateString)
        currentDate = currentDate + one_day
        dateString = str(currentDate.month)+"/"+str(currentDate.day)+"/"+str(currentDate.strftime("%y"))
    
    return dateList


def TopList(number, returnFormat):
    """
    Returns a dataframe or JSON object of the top 'number' countries and their individual stats on which the API has information
    """

    # Contact API
    try:
        response = requests.get("https://corona.lmao.ninja/v2/countries")
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        countryStats = response.json()
        countryNames = []
        rankingsDeaths = []
        rankingsCases = []
        rankingsDeathsOneMLN = []
        rankingsCasesOneMLN = []
        rankingsTestsOneMLN = []

    # construct a list for each of the elements we need.
        for i in range(len(countryStats)):
            countryNames.append(countryStats[i]["country"])
            rankingsDeaths.append(countryStats[i]["deaths"])
            rankingsCases.append(countryStats[i]["cases"])
            rankingsCasesOneMLN.append(countryStats[i]["casesPerOneMillion"])
            rankingsDeathsOneMLN.append(countryStats[i]["deathsPerOneMillion"])
            rankingsTestsOneMLN.append(countryStats[i]["testsPerOneMillion"])
        
    # turn the lists into a dataframe and sort on the number of Deaths
        zippedList =  list(zip(countryNames, rankingsDeaths, rankingsCases, rankingsCasesOneMLN, rankingsDeathsOneMLN, rankingsTestsOneMLN))
        dfObj = pd.DataFrame(zippedList, columns = ['Name', 'Deaths', 'Cases', 'CasesOneMLN', 'DeathsOneMLN', 'TestsOneMLN'])
        dfObj = dfObj.sort_values(by=['Deaths'],ascending=False)
    
    # Add the rank column
        dfObj = dfObj.reset_index(drop=True)
        dfObj = dfObj.reset_index(drop=False)
        dfObj = dfObj.rename(columns = {'index':'Rank'})
    
    # decide the length of the list. Either top x or all
        if number == 'All':
            number = len(countryStats)-1
        dfObj = dfObj.iloc[0:number]

    # add the colors to the dataframe
        colors = ColorList(number)
        dfObj['Color'] = colors

    # return a dataframe or a JSON object    
        if returnFormat == 'df':
            return dfObj
        elif returnFormat == 'json':
            return dfObj.to_json(orient='records')
    except (KeyError, TypeError, ValueError):
        return None

def ColorList(number):
    """
    Returns a list with RGBA color schemes including a gradient
    """

    # initialise the basic colors, from green, light green, yellow, orange to red
    basicsTrafficLight = ['(204,50,50)','(219,123,43)','(231,180,22)','(153,193,64)','(45,201,55)']
    
    # define which set of basic colors we are going to use
    basics = basicsTrafficLight
    numIterations = (number // len(basics))+1 
    gradients = []
    colors = []

    for i in range(numIterations):
        gradients.append(round((i+1) / (numIterations + 1),2))    
    gradients.reverse()

    # contruct the list of colors to be returned
    for i in range(number):
        indexB = i // numIterations
        indexG = i % numIterations
        endString = int(basics[indexB].find(')'))
        color = 'rgba'+basics[indexB][0:endString]+','+str(gradients[indexG])+')'
        colors.append(color)

    # deletele the colors at the end of the list we no longer need
    colors=colors[0:number]
    return colors

def KPIList(country):
    """
    This function returns a list with 6 KPIs used in the Spider graph
    Cases, Deaths, Recovered, CasesPer1MLN, DeathsPer1MLN, TestsPer1MLN   
    """

    content = HeadlinesPerCountry(country)
    KPIlist = []
    KPIlist.append(content['cases'])
    KPIlist.append(content['deaths'])
    KPIlist.append(content['recovered'])
    KPIlist.append(content['casesPerOneMillion'])
    KPIlist.append(content['deathsPerOneMillion'])
    KPIlist.append(content['testsPerOneMillion'])

    return KPIlist

def SinceDayX(country):
    """
    This function returns a list with datapoints representing the 7 day average number of Deaths 
    starting on the day a country reported more than 100 Deaths cumulatively
    """

    history = HistPerCountry(country)

    # create list for the average number of deaths and initialise two support items
    averageDeaths=[]
    currentDeaths = 0
    lastDeaths=[0,0,0,0,0,0,0]

    for i in history['history']['deaths']:
        try:
            myValue = history['history']['deaths'][i]
            
            lastDeaths.pop(0)
            lastDeaths.append(max(myValue - currentDeaths,0))
            if myValue > 100:
                averageDeaths.append(round(np.mean(lastDeaths),1))

            currentDeaths = myValue

        except(KeyError):
            lastDeaths.pop(0)
            lastDeaths.append(0)
            if myValue > 100:
                averageDeaths.append(round(np.mean(lastDeaths),0))

    return averageDeaths

def WeeklyDeathsPerCountry(country):
    """
    This function takes a dictionary of daily stats and returns a list of weekly stats
    """

    basics = HistPerCountry(country)
    dates = ListOfDates(basics['history']['deaths'])
    deaths={}
    
    for i in dates:
        try:
            deaths[i] = basics['history']['deaths'][i]
        except(KeyError):
            deaths[i] = 0

    output=[]

    for i in range(len(dates)):
        if ((i+1)%7)==0:
            try:
                number = max(deaths[dates[i]]-deaths[dates[i-7]],0)
            except(KeyError):
                number = 0
            output.append(number)

    return output

def TotalDeathsEU():
    """
    This funtion returns a dataframe of weekly deaths for all the 24 countries/regions included in the 
    Euromomo dataset. 
    
    Countries included are: Austria, Belgium, Denmark, Estonia, Finland, France, Germany (Berlin and Hesse only), 
    Greece, Hungary, Ireland, Italy, Luxembourg, Malta, Netherlands, Norway, Portugal, Spain, Sweden, 
    Switzerland, UK (England, Northern Ireland, Scotland and Wales).

    We adjusted the German numbers by a factor 10.1/83.2 to adjust for the number of inhabitants in Hesse/Berlin
    """

    countries = ["Austria", "Belgium", "Denmark", "Estonia", "Finland", "France", "Germany", "Greece", "Hungary", \
    "Ireland", "Italy", "Luxembourg", "Malta", "Netherlands", "Norway", "Portugal", "Spain", "Sweden", "Switzerland", "UK"]
    correction = 10.1/83.2
    df=pd.DataFrame()
    
    for country in countries:
        cList = WeeklyDeathsPerCountry(country)
        df[country]=cList

    df['Germany'] = df['Germany'].multiply(correction).round(0)
    df['Europe24'] = df.sum(axis=1)

    return df

def formatnumber(value):
    """Format value as 1,000,000 with zero digits behind the comma."""
    return f"{value:,.0f}"

if __name__ == "__main__":
     
    rank_list = TopList(20,'df')
    print(rank_list)
    




    

