# Corona
Website about the Corona Pandamic

I started this project as part of my CS50w course on EDX.org. I have been experimenting with the following technologies and features:

Languages: Python (including Flask, Dataframes, BS4), Jinja, HTML (Bootstrap 4), Javascript (various modules)
Javascript libraries: Chart.js, Bootstrap Datatables, Twitter Typeahead
Datasources: 
    For the COVID19 API we use https://corona.lmao.ninja/ where we predominantly rely on John Hopkins University as the ultimate source.
    In addition we extract data on Excess Mortality in Europe from www.euromomo.eu.

None of the data is stores locally. We dynamically extract the data, perform the neccesary calculations and draw the charts on the fly.

The following app routes are available
Index: with acknowledgements and intro
Country: basic stats and charts for all countries (on 1 June 2020 already 214 and counting) available in the API
Rankings: a searcheable overview of the most relevant KPIs per country
Buble Chart: plotting the top 20 countries (based on number of deaths) along four axis (absolute # of deaths, test and cases per 1 million and deaths per 100k)
Compare: compareing the main stats and charts for two countries
Excess Mortality: comparing the excess mortality with the reported number of Corona deaths for 24 european regions

Whenever I got stuck I enlisted the help of friends. Special tx go to:
Rob (helping me to get the project online on Heroku)
Jurjen (helping me out on some Charts.js elements)
Hugo (helping me to get the data from Euromomo)
Other friends (for the endless list of ideas and reporting bugs)

