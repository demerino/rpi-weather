import time
import httplib
import sys
import json
import ConfigParser

from rpi_weather import RpiWeather
from led8x8icons import LED8x8ICONS

display = RpiWeather()

#-------------------------------------------------------------------------------
#  M A I N
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    display.clear_disp(0)
    display.disp_temp(97)
    display.scroll_raw64(LED8x8ICONS['RAIN'], 0)


