#!/usr/bin/env python3
# rpi_ws281x library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

# Consider lights starting in middle
# 1 player where trigger stops lights and continues series
# 2 player with above rules, 2 distinct colors, in parallel
# 2 player with above rules, 2 distinct colors, not in parallel


import time
from rpi_ws281x import *
import argparse
from random import random
from random import randint

# LED strip configuration:
LED_COUNT      = 264      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 100     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53



# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms, target):
    """Wipe color across display a pixel at a time."""
    # for i in range(strip.numPixels()):
    start = 1+((target-1)*33)
    for i in range(start-1,start+32):
        strip.setPixelColor(i, color)
        strip.show()
# put ball hit check here and use "break" to end loop
        time.sleep(wait_ms/1000.0)
		
	
def Fillall(strip, color, target):
   # for i in range(strip.numPixels()):
   start = 1+((target-1)*33)
   for i in range (start-1, start+32):
        strip.setPixelColor(i, color)
   strip.show()
   # time.sleep(0.25)

# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
	
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')
        args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    wait_ms = input("Time in seconds to hit target:\n")
    wait_ms = int(wait_ms) / 33*1000
    length = input("Time in seconds of game:\n")
    length = int(length)
    start_time = time.time()
    try:

        while True:
            # print ('Color wipe animations.')
            # clearall(strip, Color(255, 0, 0))
            target = randint(1, 8)
            pickcolor = randint(1, 3)
            # print (pickcolor)
            # colorWipe(strip, Color(0, 0, 0), wait_ms)  # Red wipe
            if pickcolor == 1:
              Fillall(strip, Color(255, 0, 0), target)
            if pickcolor == 2:
              Fillall(strip, Color(0, 255, 0), target)
            if pickcolor == 3:
                Fillall(strip, Color(0, 0, 255), target)
                colorWipe(strip, Color(0, 0, 0), wait_ms, target)
                current_time = time.time()
            if current_time-start_time > length:
               break

    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0,0,0), 264)
