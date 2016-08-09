#!/usr/bin/env python
#===============================================================================
# weather_openweather.py
#
# Get weather forecast from openweathermap.org and display as 8x8 icons.
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

OPENWEATHER_URL    = "api.openweathermap.org"
REQ_BASE    = r"/data/2.5/weather?"
CONFIG_FILE = "/home/pi/work/rpi-weather/weather.cfg"
APIKEY = None
LAT = None
LON = None

ICON_MAP = {
#   list.weather.main value             LED 8x8 icon
    "Thunderstorm":                     "STORM",
    "Drizzle":                          "SHOWERS",
    "Rain":                             "RAIN",
    "Snow":                             "SNOW",
    "Atmosphere":                       "UNKNOWN",
    "Clear":                            "SUNNY",
    "Clouds":                           "CLOUD",
    "Extreme":                          "UNKNOWN",
    "Additional":                       "UNKNOWN",
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
        
def make_openweather_request():
    """Make request to forecast.io and return data."""
    REQUEST = REQ_BASE + "lat={0}&".format(LAT) + \
                        "lon={0}&".format(LON) + \
                        "mode=json&" + \
                        "units=imperial&" + \
                        "APPID={0}".format(APIKEY)
    try:
        conn = httplib.HTTPConnection(OPENWEATHER_URL)
        conn.request("GET", REQUEST)
        resp = conn.getresponse()
        data = resp.read()
    except:
        giveup()
    else:
        return data
    
def get_forecast():
    """Return a list of forecast results."""
    json_data = json.loads(make_openweather_request())
    print json_data
    forecast = {}
    forecast['summary'] = [json_data['weather'][0]['main']]
    forecast['temp'] = json_data['main']['temp']
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
