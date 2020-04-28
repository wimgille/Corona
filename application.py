from flask import Flask, session, render_template, request, redirect, jsonify, json
from flask_session import Session
from helpers import TopList, CountryList,HeadlinesPerCountry,CountryList,HistPerCountry,ConvertToList
from helpers import ColorList,ListOfDates,HistPerCountryLong

app = Flask(__name__)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/country", methods=["GET"])
def countryGet():
    """get an overview of the key stats per country"""
    
    # User reached route via GET
    if request.method == "GET":
        
        countryList = CountryList()
        return render_template("countryGET.html", countryList=countryList)
        
    # User reached route via POST
    else:
        return render_template("apology.html", message="Method not allowed"), 405

@app.route("/country/<string:country>", methods=["GET"])
def country(country):
    
    # User reached route via GET
    if request.method == "GET":
        
        content = HeadlinesPerCountry(country)
        countryList = CountryList()
        
        history = HistPerCountryLong(country)
        deaths = ConvertToList(history["history"]["deaths"])
        newdeaths = ConvertToList(history["history"]["newDeaths"])
        cases = ConvertToList(history["history"]["cases"])
        newcases = ConvertToList(history["history"]["newCases"])
        dates = ListOfDates(history["history"]["deaths"])
        
        return render_template("country.html", content=content, countryList=countryList, newdeaths=newdeaths, deaths=deaths, dates=dates, cases=cases, newcases=newcases)
       
    # User reached route via POST
    else:
        return render_template("apology.html", message="Method not allowed"), 405

@app.route("/graph")
def graph():

    numberCountries = 20

    rankingsJSON = TopList(numberCountries,'json')
    rankingsJSON = json.loads(rankingsJSON)
    return render_template("graph_bubble.html",countries=rankingsJSON)

@app.route("/rankings")
def rankings():

    rankingsJSON = TopList('All','json')
    rankingsJSON = json.loads(rankingsJSON)
    return render_template("rankings.html", countries=rankingsJSON)

@app.route("/compare/<string:country>", methods=["GET"])
def compare(country):
    
    # User reached route via GET
    if request.method == "GET":
        
        countryList = CountryList()
        if country not in countryList:
            country = 'Italy'

        history = HistPerCountryLong(country)
        deaths = ConvertToList(history["history"]["deathsPerOneMLN"])
        cases = ConvertToList(history["history"]["casesPerOneMLN"])
        newdeaths = ConvertToList(history["history"]["newDeaths"])
        newcases = ConvertToList(history["history"]["newCases"])

        historyNL = HistPerCountryLong('Netherlands')
        deathsNL = ConvertToList(historyNL["history"]["deathsPerOneMLN"])
        casesNL = ConvertToList(historyNL["history"]["casesPerOneMLN"])
        newdeathsNL = ConvertToList(historyNL["history"]["newDeaths"])
        newcasesNL = ConvertToList(historyNL["history"]["newCases"])
        dates = ListOfDates(history["history"]["cases"])


        return render_template("compare.html", country=country, countryList=countryList, deaths=deaths, deathsNL=deathsNL, newdeaths=newdeaths, \
        newdeathsNL=newdeathsNL, casesNL=casesNL, newcasesNL=newcasesNL, newcases=newcases, cases=cases, dates=dates)
       
    # User reached route via POST
    else:
        return render_template("apology.html", message="Method not allowed"), 405




