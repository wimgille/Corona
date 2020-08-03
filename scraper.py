#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This will be the helper file that will contain the functions for 
1) Scraping external webistes
2) to be defined
"""

import requests
import json
from bs4 import BeautifulSoup
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
import re
import ast
import pandas as pd

import re
import urllib
from urllib.request import Request, urlopen


 
def ExcessMort():
    """
    This function will load the mortality data from the Euromomo website for 24 European countries
    Countries included are: Austria, Belgium, Denmark, Estonia, Finland, France, Germany (Berlin), 
    Germany (Hesse), Greece, Hungary, Ireland, Italy, Luxembourg, Malta, Netherlands, Norway, Portugal, 
    Spain, Sweden, Switzerland, UK (England), UK (Northern Ireland), UK (Scotland), UK (Wales).   
    
    The function returns a dataframe containing 57 collums including Date and 7 attributes [zscore, 
    total deaths, baseline, excess deaths, substantial increase, high and low end of normakl range] 
    over 7 age brackets [0 to 4, 5 to 14, 15 to 64, 65 to 74, 75 to 84, 85 plus, 65 plus and total]
    """

    # prepare the headers and collect the Request URL that sources the website.
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "referer": "https://www.euromomo.eu/graphs-and-maps/",
        "sec-fetch-dest": "script",
        "sec-fetch-mode": "no-cors",
        "sec-fetch-site": "same-origin"}

    s=requests.session()

    myURL = FindURL()
    if (myURL == 'Not Found'):
        myURL = 'https://www.euromomo.eu/component---src-templates-graphs-and-maps-js-32b0c7c01e7ecdb2bd68.js'

    r = s.get(myURL, headers=headers).text
    # week 20 https://www.euromomo.eu/component---src-templates-graphs-and-maps-js-1fb13ae0d6683c6d2b12.js
    # week 21 https://www.euromomo.eu/component---src-templates-graphs-and-maps-js-c9af76ec69719f4fd96a.js
    # week 23 https://www.euromomo.eu/component---src-templates-graphs-and-maps-js-25b37370cda3f45b1802.js
    # week 30 https://www.euromomo.eu/component---src-templates-graphs-and-maps-js-32b0c7c01e7ecdb2bd68.js


    # strip the textfile and isolate the right JSON object
    sourceText = r.split('{e.exports=JSON.parse(')
    text = sourceText[2].split(',zTTH:function(e,t,n)')[0]
    new=text[1:-3]
    data=json.loads(new)

    # prepare the colums in 50 different lists
    date = data["pooled"]["weeks"]

    zscore_0to14 = data["pooled"]["groups"][0]['zscore']
    total_number_deaths_0to14 = data["pooled"]["groups"][0]['nbc']
    baseline_deaths_0to14 = data["pooled"]["groups"][0]['pnb']
    excess_deaths_0to14 = data["pooled"]["groups"][0]['excess']
    si_deaths_0to14 = data["pooled"]["groups"][0]['si']
    hnr_deaths_0to14 = data["pooled"]["groups"][0]['hnr']
    lnr_deaths_0to14 = data["pooled"]["groups"][0]['lnr']

    zscore_15to44 = data["pooled"]["groups"][1]['zscore']
    total_number_deaths_15to44 = data["pooled"]["groups"][1]['nbc']
    baseline_deaths_15to44 = data["pooled"]["groups"][1]['pnb']
    excess_deaths_15to44 = data["pooled"]["groups"][1]['excess']
    si_deaths_15to44 = data["pooled"]["groups"][1]['si']
    hnr_deaths_15to44 = data["pooled"]["groups"][1]['hnr']
    lnr_deaths_15to44 = data["pooled"]["groups"][1]['lnr']

    zscore_45to64 = data["pooled"]["groups"][2]['zscore']
    total_number_deaths_45to64 = data["pooled"]["groups"][2]['nbc']
    baseline_deaths_45to64 = data["pooled"]["groups"][2]['pnb']
    excess_deaths_45to64 = data["pooled"]["groups"][2]['excess']
    si_deaths_45to64 = data["pooled"]["groups"][2]['si']
    hnr_deaths_45to64 = data["pooled"]["groups"][2]['hnr']
    lnr_deaths_45to64 = data["pooled"]["groups"][2]['lnr']

    zscore_65P = data["pooled"]["groups"][3]['zscore']
    total_number_deaths_65P = data["pooled"]["groups"][3]['nbc']
    baseline_deaths_65P = data["pooled"]["groups"][3]['pnb']
    excess_deaths_65P = data["pooled"]["groups"][3]['excess']
    si_deaths_65P = data["pooled"]["groups"][3]['si']
    hnr_deaths_65P = data["pooled"]["groups"][3]['hnr']
    lnr_deaths_65P = data["pooled"]["groups"][3]['lnr']

    zscore_65to74 = data["pooled"]["groups"][4]['zscore']
    total_number_deaths_65to74 = data["pooled"]["groups"][4]['nbc']
    baseline_deaths_65to74 = data["pooled"]["groups"][4]['pnb']
    excess_deaths_65to74 = data["pooled"]["groups"][4]['excess']
    si_deaths_65to74 = data["pooled"]["groups"][4]['si']
    hnr_deaths_65to74 = data["pooled"]["groups"][4]['hnr']
    lnr_deaths_65to74 = data["pooled"]["groups"][4]['lnr']

    zscore_75to84 = data["pooled"]["groups"][5]['zscore']
    total_number_deaths_75to84 = data["pooled"]["groups"][5]['nbc']
    baseline_deaths_75to84 = data["pooled"]["groups"][5]['pnb']
    excess_deaths_75to84 = data["pooled"]["groups"][5]['excess']
    si_deaths_75to84 = data["pooled"]["groups"][5]['si']
    hnr_deaths_75to84 = data["pooled"]["groups"][5]['hnr']
    lnr_deaths_75to84 = data["pooled"]["groups"][5]['lnr']

    zscore_85P = data["pooled"]["groups"][6]['zscore']
    total_number_deaths_85P = data["pooled"]["groups"][6]['nbc']
    baseline_deaths_85P = data["pooled"]["groups"][6]['pnb']
    excess_deaths_85P = data["pooled"]["groups"][6]['excess']
    si_deaths_85P = data["pooled"]["groups"][6]['si']
    hnr_deaths_85P = data["pooled"]["groups"][6]['hnr']
    lnr_deaths_85P = data["pooled"]["groups"][6]['lnr']

    zscore_tot = data["pooled"]["groups"][7]['zscore']
    total_number_deaths_tot = data["pooled"]["groups"][7]['nbc']
    baseline_deaths_tot = data["pooled"]["groups"][7]['pnb']
    excess_deaths_tot = data["pooled"]["groups"][7]['excess']
    si_deaths_tot = data["pooled"]["groups"][7]['si']
    hnr_deaths_tot = data["pooled"]["groups"][7]['hnr']
    lnr_deaths_tot = data["pooled"]["groups"][7]['lnr']

    # and merge all the list into a dataframe
    df=pd.DataFrame({"Date":date, "zscore_tot":zscore_tot, "total_number_deaths_tot":total_number_deaths_tot, "baseline_deaths_tot":baseline_deaths_tot, "excess_deaths_tot":excess_deaths_tot, "si_deaths_tot": si_deaths_tot, "hnr_deaths_tot":hnr_deaths_tot, "lnr_deaths_tot": lnr_deaths_tot, \
        "zscore_0to14":zscore_0to14, "total_number_deaths_0to14":total_number_deaths_0to14, "baseline_deaths_0to14":baseline_deaths_0to14, "excess_deaths_0to14":excess_deaths_0to14, "si_deaths_0to14": si_deaths_0to14, "hnr_deaths_0to14":hnr_deaths_0to14, "lnr_deaths_0to14": lnr_deaths_0to14, \
        "zscore_15to44":zscore_15to44, "total_number_deaths_15to44":total_number_deaths_15to44, "baseline_deaths_15to44":baseline_deaths_15to44, "excess_deaths_15to44":excess_deaths_15to44, "si_deaths_15to44": si_deaths_15to44, "hnr_deaths_15to44":hnr_deaths_15to44, "lnr_deaths_15to44": lnr_deaths_15to44, \
        "zscore_45to64":zscore_45to64, "total_number_deaths_45to64":total_number_deaths_45to64, "baseline_deaths_45to64":baseline_deaths_45to64, "excess_deaths_45to64":excess_deaths_45to64, "si_deaths_45to64": si_deaths_45to64, "hnr_deaths_45to64":hnr_deaths_45to64, "lnr_deaths_45to64": lnr_deaths_45to64, \
        "zscore_65P":zscore_65P, "total_number_deaths_65P":total_number_deaths_65P, "baseline_deaths_65P":baseline_deaths_65P, "excess_deaths_65P":excess_deaths_65P, "si_deaths_65P": si_deaths_65P, "hnr_deaths_65P":hnr_deaths_65P, "lnr_deaths_65P": lnr_deaths_65P, \
        "zscore_65to74":zscore_65to74, "total_number_deaths_65to74":total_number_deaths_65to74, "baseline_deaths_65to74":baseline_deaths_65to74, "excess_deaths_65to74":excess_deaths_65to74, "si_deaths_65to74": si_deaths_65to74, "hnr_deaths_65to74":hnr_deaths_65to74, "lnr_deaths_65to74": lnr_deaths_65to74, \
        "zscore_75to84":zscore_75to84, "total_number_deaths_75to84":total_number_deaths_75to84, "baseline_deaths_75to84":baseline_deaths_75to84, "excess_deaths_75to84":excess_deaths_75to84, "si_deaths_75to84": si_deaths_75to84, "hnr_deaths_75to84":hnr_deaths_75to84, "lnr_deaths_75to84": lnr_deaths_75to84, \
        "zscore_85P":zscore_85P, "total_number_deaths_85P":total_number_deaths_85P, "baseline_deaths_85P":baseline_deaths_85P, "excess_deaths_85P":excess_deaths_85P, "si_deaths_85P": si_deaths_85P, "hnr_deaths_85P":hnr_deaths_85P, "lnr_deaths_85P": lnr_deaths_85P})
    
    return df

def FindURL():
    """
    This function looks up the right javascript object that contains the actual data. The script elements 
    contained a double quotes, which required regular expressions to extract the right text components.
    The funtion returns the target URL. If no URL has been found the funtion returns 'Not Found'
    """

    # inittialise the right variables
    myURL = "https://www.euromomo.eu/graphs-and-maps"    
    targetURL = 'Not Found'
    
    # create a list of strings for each script element on the website
    response = urllib.request.urlopen(myURL).read()
    myScript = re.findall('<script((.|\s)+?)</script>', str(response)) #(pattern, string)

    # search for the right element and create a target URL containing the right js object
    for script in myScript:
        if "/component---src-templates-graphs-and-maps-js-" in str(script):
            target = str(script)

    targetList = target.split('"')
    
    for item in targetList:
        if "/component---src-templates-graphs-and-maps-js-" in item:
            targetURL = 'https://www.euromomo.eu'+item

    return targetURL

if __name__ == "__main__":
    source = ExcessMort()
    print(source)
    print('done')
    
   

