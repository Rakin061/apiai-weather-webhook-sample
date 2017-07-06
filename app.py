#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") == "yahooWeatherForecast":

        baseurl = "https://query.yahooapis.com/v1/public/yql?"
        yql_query = makeYqlQuery(req)
        if yql_query is None:
            return {}
        yql_url = baseurl + urlencode({'q': yql_query}) + "&format=json"
        result = urlopen(yql_url).read()
        data = json.loads(result)
        res = makeWebhookResult(data)
        return res

    elif req.get("result").get("action") == "loan.eligibilty":

        result = req.get("result")
        parameters = result.get("parameters")
        zone = str(parameters.get("Numbers"))

        zone = zone.strip()
        # zone= int(zone)
        # val= int(zone)

        # condition['zone'] = int(zone)

        # cost = {'Europe':100, 'North America':200, 'South America':300, 'Asia':400, 'Africa':500}
        # if zone is not None and zone.isnumeric():
        if int(zone) > 25000:
            speech = "Congratulation, Sir. You are eligible for loan"
        else:
            speech = "We're Sorry, Sir. You are not eligible for loan"

        print("Response:")
        print(speech)

        return {
            "speech": speech,
            "displayText": speech,
            # "data": {},
            # "contextOut": [],
            "source": "apiai-onlinestore-shipping"
        }

    

    else:
        return {}

def makeYqlQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    if city is None:
        return None

    return "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "')"


def makeWebhookResult(data):
    query = data.get('query')
    if query is None:
        return {}

    result = query.get('results')
    if result is None:
        return {}

    channel = result.get('channel')
    if channel is None:
        return {}

    item = channel.get('item')
    location = channel.get('location')
    units = channel.get('units')
    if (location is None) or (item is None) or (units is None):
        return {}

    condition = item.get('condition')
    if condition is None:
        return {}

    # print(json.dumps(item, indent=4))

    temp= condition.get('temp')
    temp=int(temp)
    temp = ((temp-32)*5)/9
    temp=str(temp)


    speech = " Hello!! Today the weather in " + location.get('city') + " is : " + condition.get('text') + \
             ", and the temperature is " + temp + " " + "C" + ".  Thanks!!"

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
