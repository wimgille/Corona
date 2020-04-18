from flask import Flask, session, render_template, request, redirect, jsonify, json
from flask_session import Session
from helpers import TopList, CountryList,HeadlinesPerCountry,CountryList,HistPerCountry,ConvertToList,ListOfDates,Rankings

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
        
        history = HistPerCountry(country)
        deaths = ConvertToList(history["history"]["deaths"])
        cases = ConvertToList(history["history"]["cases"])
        dates = ListOfDates(history["history"]["deaths"])

        return render_template("country.html", content=content, countryList=countryList, deaths=deaths, dates=dates, cases=cases)
        
        
    # User reached route via POST
    else:
        return render_template("apology.html", message="Method not allowed"), 405

@app.route("/graph")
def graph():

    rankingsJSON = TopList(20,'json')
    rankingsJSON = json.loads(rankingsJSON)
    return render_template("graph_new.html",countries=rankingsJSON)

@app.route("/rankings")
def rankings():

    rankingsJSON = Rankings('json')
    return render_template("rankings.html", countries=rankingsJSON)