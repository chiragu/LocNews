# LocNews
# Author: Chirag Uttamsingh
# Date: 11/24/2018

# Flask Web App for News Website based on Location
# Uses the NewsAPI from NewsAPI.org 

# import Flask class, html template renderer, request for geolocation, ppprint for test printing JSON 
from flask import Flask, render_template, request, url_for
import requests
from urllib import urlopen
import json
import re
from pprint import pprint

# API Key - Remove from code posted to GitHub!
APIKey = '<Removed - Put your NewsAPI Key here>'

# Create a Flask object called 'app' passing in the name
# __name__ is name of module
# __name__ = __main__
app = Flask(__name__)


# Routes - what we type into a browser to go to different pages
@app.route('/news')  #route decorator - info that will be shown at /news
def news():

    # Call API and get news JSON object
    country = getUserLocation()

    # Call News API to get news
    pythonNews = newsAPI(country)

    # Get the articles from the news
    pythonArticles = pythonNews['articles']

    # Test print of articles in python dictionary
    #pprint (pythonArticles)

    # Pass the news to the template to render
    return render_template('news.html', news=pythonArticles)

# Helper functions ##############################################

# Get users location - this is currently country
def getUserLocation():
    # Use Geolocation service to get users country
    url = 'http://ipinfo.io/json'
    response = urlopen(url)
    data = json.load(response)

    IP=data['ip']
    org=data['org']
    city = data['city']
    country=data['country']
    region=data['region']

    #print 'Your IP detail\n '
    #print 'IP : {4} \nRegion : {1} \nCountry : {2} \nCity : {3} \nOrg : {0}'.format(org,region,country,city,IP)

    return country

# Call news API with location code and returns a python dict with the news
def newsAPI(country):

    url = 'https://newsapi.org/v2/top-headlines?country=' + country
    headers = {'x-api-key':APIKey}
    r = requests.get(url, headers=headers)

    # Catch if request fails
    if r.status_code != requests.codes.ok:
        raise NewsAPIException(r.json())
    
    # test print of JSON
    #print(json.dumps(r.json(), indent=2))

    # Conver JSON to Python dictionary
    python_news = json.loads(json.dumps(r.json()))

    return python_news


# if we run the script with python directly
if __name__ =='__main__':
    app.run()

