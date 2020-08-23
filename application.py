from flask import Flask, session, render_template, request, redirect, jsonify, json
#from flask_session import Session
from helpers import TopList, CountryList,HeadlinesPerCountry,HistPerCountry,ConvertToList
from helpers import ColorList,ListOfDates,HistPerCountryLong,KPIList,SinceDayX,TotalDeathsEU
from americas import StatesList,HeadlinesPerStateWM, ConvertWMtoJH, HistPerState, HistPerStateLong
from scraper import ExcessMort

app = Flask(__name__)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
#Session(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/country", methods=["GET"])
def countryGet():
    """get an overview of the key stats per country get the country"""
    
    # User reached route via GET
    if request.method == "GET":
        
        countryList = CountryList()
        return render_template("countryGET.html", countryList=countryList)
        
    # User reached route via POST
    else:
        return render_template("apology.html", message="Method not allowed"), 405

@app.route("/country/<string:country>", methods=["GET"])
def country(country):
    """get an overview of the key stats per country display"""
    
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
    """displays a bubble chart with four dimensions for each of the top countries"""

    numberCountries = 25

    rankingsJSON = TopList(numberCountries,'json')
    rankingsJSON = json.loads(rankingsJSON)
    return render_template("graph_bubble.html",countries=rankingsJSON)

@app.route("/rankings")
def rankings():
    """displays a table with the key KPIs for each country"""

    rankingsJSON = TopList('All','json')
    rankingsJSON = json.loads(rankingsJSON)
    return render_template("rankings.html", countries=rankingsJSON)


@app.route("/compare", methods=["GET", "POST"])
def compare():
    """compare two countries"""
    
    # User reached route via GET
    if request.method == "GET":
        
        countryList = CountryList()
        return render_template("getCompare.html", countryList=countryList)
        
    # User reached route via POST
    elif request.method == "POST":

        # Check if the user included two separate companies
        if not request.form.get("country1"):
            return render_template("apology.html", message="must provide two countries to compare"), 400
        
        if not request.form.get("country2"):
            return render_template("apology.html", message="must provide two countries to compare"), 400
        
        country1 = request.form.get("country1")
        country2 = request.form.get("country2")

        # Check if the user typed two countries that are actually in the list
        countryList = CountryList()
        if country1 in countryList and country2 in countryList:
            
            # Collect the right data lists for both companies.
            history = HistPerCountryLong(country1)
            deaths = ConvertToList(history["history"]["deathsPerOneMLN"])
            cases = ConvertToList(history["history"]["casesPerOneMLN"])
            newdeaths = ConvertToList(history["history"]["newDeaths"])
            newcases = ConvertToList(history["history"]["newCases"])
            avgdeaths = SinceDayX(country1)
            dates = ListOfDates(history["history"]["cases"])

            history2 = HistPerCountryLong(country2)
            deaths2 = ConvertToList(history2["history"]["deathsPerOneMLN"])
            cases2 = ConvertToList(history2["history"]["casesPerOneMLN"])
            newdeaths2 = ConvertToList(history2["history"]["newDeaths"])
            newcases2 = ConvertToList(history2["history"]["newCases"])
            avgdeaths2 = SinceDayX(country2)
            
            # Resize the KPI lists and rebase them to 100%
            KPIcountry1 = KPIList(country1)
            KPIcountry2 = KPIList(country2)
            for i in range(len(KPIcountry1)):
                maxKPI = max(KPIcountry1[i],KPIcountry2[i])
                if maxKPI == 0:
                    KPIcountry1[i]=0
                    KPIcountry2[i]=0
                else:
                    KPIcountry1[i]=(KPIcountry1[i]/maxKPI)*100
                    KPIcountry2[i]=(KPIcountry2[i]/maxKPI)*100

            # Make labels for the line chart
            maxLength = max(len(avgdeaths),len(avgdeaths2))
            labels = []
            for i in range(maxLength):
                labels.append(i+1)
            
            return render_template("compare.html", country1=country1, country2 = country2, countryList=countryList, deaths=deaths, deaths2=deaths2, \
            newdeaths=newdeaths, newdeaths2=newdeaths2, cases=cases, cases2=cases2, newcases2=newcases2, newcases=newcases, dates=dates, \
            KPIcountry1=KPIcountry1, KPIcountry2=KPIcountry2, avgdeaths=avgdeaths, avgdeaths2=avgdeaths2, labels=labels)

        else:
            return render_template("apology.html", message="unknown country"), 400

    else:
        return render_template("apology.html", message="method not allowed"), 405


@app.route("/ExcessMortality")
def excess_mort():
    """Comparing the official Corona stats with excess mortality in Europe"""
    
    # the graphs start in the summer of 2016
    start=0 
    source = ExcessMort()
    totalDeaths = source['total_number_deaths_tot'][start:]
    baseline = source['baseline_deaths_tot'][start:]
    excess = source['excess_deaths_tot'][start:]
    dates = source['Date'][start:]
    
    # to compare with the corona stats we start on 1 Jan 2020
    Nr = list(dates).index("2020-01")
    totalDeaths20 = totalDeaths[Nr:]
    baseline20 = baseline[Nr:]
    dates20 = dates[Nr:]
    excess20 = excess[Nr:]
    corona20 = TotalDeathsEU()
    corona20 = corona20['Europe24']

    return render_template("euromomo.html", deaths=totalDeaths, dates=dates, baseline=baseline, dates20=dates20, excess20=excess20, corona20=corona20)

@app.route("/states", methods=["GET"])
def statesGet():
    """get the list of all US states"""
    
    # User reached route via GET
    if request.method == "GET":
        
        stateList = StatesList()
        return render_template("statesGET.html", stateList=stateList)
        
    # User reached route via POST
    else:
        return render_template("apology.html", message="Method not allowed"), 405

@app.route("/states/<string:state>", methods=["GET"])
def state(state):
    """get an overview of the key stats per US state"""
    
    # User reached route via GET
    if request.method == "GET":
        
        stateWM = ConvertWMtoJH('JH', state)
        content = HeadlinesPerStateWM(stateWM)
        stateList = StatesList()
        
        history = HistPerStateLong(state)
        deaths = ConvertToList(history["history"]["deaths"])
        newdeaths = ConvertToList(history["history"]["newDeaths"])
        cases = ConvertToList(history["history"]["cases"])
        newcases = ConvertToList(history["history"]["newCases"])
        dates = ListOfDates(history["history"]["deaths"])
        
        return render_template("us_states.html", content=content, stateList=stateList, newdeaths=newdeaths, deaths=deaths, dates=dates, cases=cases, newcases=newcases)
       
    # User reached route via POST
    else:
        return render_template("apology.html", message="Method not allowed"), 405
