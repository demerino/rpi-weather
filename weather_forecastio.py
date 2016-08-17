#!/usr/bin/env python
#===============================================================================
# weather_forecastio.py
#
# Get weather forecast from forecast.io and display as 8x8 icons.
#
# 2016-07-27
# Carter Nelson
#===============================================================================
import time
import httplib
import sys
import json
import ConfigParser

from rpi_weather import RpiWeather
from led8x8icons import LED8x8ICONS

display = RpiWeather()

FORECASTIO_URL    = "api.forecast.io"
REQ_BASE    = r"/forecast/"
CONFIG_FILE = "/home/pi/work/rpi-weather/weather.cfg"
APIKEY = None
LAT = None
LON = None

ICON_MAP = {
#   forecast.io icon value              LED 8x8 icon
    "clear-day":                        "SUNNY",
    "clear-night":                      "MOON",
    "rain":                             "RAIN",
    "snow":                             "SNOW",
    "sleet":                            "STORM",
    "wind":                             "KANJI_3",
    "fog":                              "KANJI_8",
    "cloudy":                           "CLOUD",
    "partly-cloudy-day":                "CLOUD",
    "partly-cloudy-night":              "CLOUD",
}

def giveup():
    """Action to take if anything bad happens."""
    for matrix in xrange(1):
        display.set_raw64(LED8x8ICONS['UNKNOWN'],matrix)
    print "Error occured."
    sys.exit(1)
    
def read_config(filename):
    config = ConfigParser.RawConfigParser()
    global APIKEY, LAT, LON
    try:
        config.read(filename)
        APIKEY = config.get('config','APIKEY')
        LAT = config.get('config','LAT')
        LON = config.get('config','LON')
    except:
        giveup()
        
def make_forecastio_request():
    """Make request to forecast.io and return data."""
    REQUEST = REQ_BASE + "{0}/".format(APIKEY)+\
                        "{0},{1}".format(LAT,LON)
    try:
        conn = httplib.HTTPSConnection(FORECASTIO_URL)
        conn.request("GET", REQUEST)
        resp = conn.getresponse()
        data = resp.read()
    except:
        giveup()
    else:
        return data
    
def get_forecast():
    """Return a list of forecast results."""
    json_data = json.loads(make_forecastio_request())
   
    forecast = {}
    forecast['summary'] = [json_data['currently']['icon']]
    forecast['temp'] = json_data['currently']['temperature']
    return forecast
    
def print_forecast(forecast=None):
    """Print forecast to screen."""
    if forecast == None:
        return
    print '-'*20
    print time.strftime('%Y/%m/%d %H:%M:%S')
    print "LAT: {0}  LON: {1}".format(LAT,LON)
    print '-'*20
    for daily in forecast:
        print daily

def display_forecast(forecast=None):
    """Display forecast as icons on LED 8x8 matrices."""
    if forecast == None:
        return
    for matrix in xrange(1):
        try:
            icon = ICON_MAP[forecast[matrix]]
            display.scroll_raw64(LED8x8ICONS[icon], matrix)
        except:
            display.scroll_raw64(LED8x8ICONS["UNKNOWN"], matrix)

#-------------------------------------------------------------------------------
#  M A I N
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    read_config(CONFIG_FILE)
    forecast = get_forecast()
    print forecast
    print_forecast(forecast['summary'])
    display.clear_disp(0)
    display.disp_temp(forecast['temp'])
    display_forecast(forecast['summary'])
