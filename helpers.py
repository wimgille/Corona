#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This will be the helper file that will contain the functions for 
1) Loading new statistics per country
2) TO BE DEFINED
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
    Look up historical statistics per country. Function returns a dics with 
    {"standardizedCountryName":"netherlands","history":{
    "cases":{"1/22/20":0,"1/23/20":0},
    "deaths":{"1/22/20":0,"1/23/20":0},
    "recovered":{"1/22/20":0,"1/23/20":0}
    }}   
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

def HeadlinesPerCountry(country):
    """
    Look up headline statistics per country. Function returns a dics with 
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

def Rankings(returnFormat):
    """
    Returns a dataframe or JSON obejct of all countries and their individual stats on which the API has information
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

        for i in range(len(countryStats)):
            countryNames.append(countryStats[i]["country"])
            rankingsDeaths.append(countryStats[i]["deaths"])
            rankingsCases.append(countryStats[i]["cases"])
            rankingsCasesOneMLN.append(countryStats[i]["casesPerOneMillion"])
            rankingsDeathsOneMLN.append(countryStats[i]["deathsPerOneMillion"])

        zippedList =  list(zip(countryNames, rankingsDeaths, rankingsCases, rankingsDeathsOneMLN, rankingsCasesOneMLN))
        dfObj = pd.DataFrame(zippedList, columns = ['Name', 'Deaths', 'Cases', 'CasesOneMLN', 'DeathsOneMLN'])
        if returnFormat == 'df':
            return dfObj
        elif returnFormat == 'json':
            return countryStats
    except (KeyError, TypeError, ValueError):
        return None

def TopList(number, returnFormat):
    """
    Returns a dataframe or JSON object of the top xx countries and their individual stats on which the API has information
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

        for i in range(len(countryStats)):
            countryNames.append(countryStats[i]["country"])
            rankingsDeaths.append(countryStats[i]["deaths"])
            rankingsCases.append(countryStats[i]["cases"])
            rankingsCasesOneMLN.append(countryStats[i]["casesPerOneMillion"])
            rankingsDeathsOneMLN.append(countryStats[i]["deathsPerOneMillion"])
            rankingsTestsOneMLN.append(countryStats[i]["testsPerOneMillion"])

        zippedList =  list(zip(countryNames, rankingsDeaths, rankingsCases, rankingsCasesOneMLN, rankingsDeathsOneMLN, rankingsTestsOneMLN))
        dfObj = pd.DataFrame(zippedList, columns = ['Name', 'Deaths', 'Cases', 'CasesOneMLN', 'DeathsOneMLN', 'TestsOneMLN'])
        dfObj = dfObj.sort_values(by=['Deaths'],ascending=False)
        dfObj = dfObj.iloc[0:number]
        
        if returnFormat == 'df':
            return dfObj
        elif returnFormat == 'json':
            return dfObj.to_json(orient='records')
    except (KeyError, TypeError, ValueError):
        return None


if __name__ == "__main__":
    
    rankingsTotal = TopList(30, 'json')
    rankingsTotal = json.loads(rankingsTotal)
    
    rankingsTotal2 = Rankings('json')
    print(rankingsTotal)


    

