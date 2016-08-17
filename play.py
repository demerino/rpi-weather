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
    	BITMAP = [
	[0, 0, 0, 1, 1, 0, 0, 0,],
	[0, 0, 1, 0, 0, 1, 0, 0,],
	[0, 1, 0, 0, 1, 0, 0, 0,],
	[1, 0, 0, 1, 0, 0, 1, 0,],
	[1, 0, 0, 1, 0, 0, 0, 0,],
	[0, 1, 0, 0, 1, 0, 0, 0,],
	[0, 0, 1, 0, 0, 1, 0, 0,],
	[0, 0, 0, 1, 1, 0, 0, 0,],
	]
	value = 0
	for y,row in enumerate(BITMAP):
    		row_byte = 0
    		for x,bit in enumerate(row):
       			row_byte += bit<<x    
    		value += row_byte<<(8*y)
	print '0x'+format(value,'02x')

    #display.clear_disp(0)
    #display.disp_temp(97)
    #display.scroll_raw64(LED8x8ICONS['RAIN'], 0)


