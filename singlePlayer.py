# Single Player Mode

# 1 player game
# Targets light up for a set amount of time
# If the target is hit before time expires, add a point to the score and go to the next target
# If time expires, go to the next target
# Targets are chosen in random order
# Run for a set duration of time




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

# Other Constants
LED_PER_TARGET = 33
NUM_TARGERTS = 8



# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms, target, points = 0):
    """Wipe color across display a pixel at a time."""
    start = target*LED_PER_TARGET

    for i in range(start, start + LED_PER_TARGET):
        strip.setPixelColor(i, color)
        strip.show()

        if (piezoceramics[target]):
            points+=1
            print("Target hit. New score is " + points)
            break

        time.sleep(wait_ms/1000.0)
	
def fillAll(strip, color, target):
    """Instantly change color of pixels in target range"""
    start = target*LED_PER_TARGET

    for i in range(start, start + LED_PER_TARGET):
        strip.setPixelColor(i, color)

    strip.show()

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

    # Variables
    piezoceramics = [0, 0, 0, 0, 0, 0, 0, 0] # Array of piezocermaic objects (just 0s for now, add whatever read method later when fixed)
    score = 0

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')
        args = parser.parse_args()

    # Create NeoPixel object
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)

    # Intialize NeoPixel
    strip.begin()

    #Initialize pizo ceramics and add to array

    # Termination Condition
    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')
    
    # User Input
    wait_ms = input("Time in seconds to hit target:\n")
    wait_ms = int(wait_ms) / LED_PER_TARGET*1000 
    length = input("Time in seconds of game:\n")
    length = int(length)
    start_time = time.time()


    try:
        while True:
            # Pick random target and color
            target = randint(0, NUM_TARGERTS - 1)
            pickcolor = randint(1, 3)

            # Color Lights based on target
            if pickcolor == 1:
                fillAll(strip, Color(255, 0, 0), target)
            if pickcolor == 2:
                fillAll(strip, Color(0, 255, 0), target)
            if pickcolor == 3:
                fillAll(strip, Color(0, 0, 255), target)
            
            # Reset light color
            colorWipe(strip, Color(0, 0, 0), wait_ms, target, score)

            # Check if time has expired and terminate if it has
            current_time = time.time()
            if current_time-start_time > length:
               break

    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0,0,0), 264)
