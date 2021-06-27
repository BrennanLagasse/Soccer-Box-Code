# Single Player Mode


# General Rules
# A player is awared a point for hitting their designated target while the lights are still on
# Targets' lights are on for a limited amount of time
# After a target is triggered or time expires, a new unused target is selected as the designated target
# The game lasts a set amount of time after which all lights turn off
# Scores are displayed via the OLED

# One Player Mode
# One designated target on at a time

# Two Player Simultaneous Mode
# Each player has a designated target on at a time

# Two Player First Person Scores (Competitive) Mode
# Each player has a designated target on at a time
# If either designated target is triggered, two new designated targets are selected




# Game functionality
import time
from random import random
from random import randint
import argparse

# Lights
from rpi_ws281x import *


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

def limitedInput(prompt, acceptableAnswers):
    """Takes user input and reasks the user when an unacceptable answer is given"""

    while True:
        response = input(prompt)

        if response in acceptableAnswers:
            return response
        else:
            print("Invalid input.")

# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create and initialize RGB lights
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()

    # Create and store Piezoceramic objects (research this)
    piezoceramics = [0, 0, 0, 0, 0, 0, 0, 0] # Array of piezocermaic objects (just 0s for now, add whatever read method later when fixed)

    # Other variables
    score = 0

    # Termination Condition
    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')
    
    # User Input
    num_players = int(limitedInput("Number of players (1 or 2):\n", [ "1", "2"]))

    if(num_players == 2):
        competitive = limitedInput("First person scores (y/n):\n", ["y", "n"])
        print("For two player, player 1 will get the red goals and player 2 will get the blue goals.")

    target_length = int(input("Time in seconds to hit target:\n")) / LED_PER_TARGET*1000 

    game_length = int(input("Time in seconds of game:\n"))

    start_time = time.time()


    try:
        while True:
            # Pick random target and color
            target = randint(1, NUM_TARGERTS) - 1
            pickcolor = randint(1, 3)

            # Color Lights based on target
            if pickcolor == 1:
                fillAll(strip, Color(255, 0, 0), target)
            if pickcolor == 2:
                fillAll(strip, Color(0, 255, 0), target)
            if pickcolor == 3:
                fillAll(strip, Color(0, 0, 255), target)
            
            # Reset light color
            colorWipe(strip, Color(0, 0, 0), target_length, target, score)

            # Check if time has expired and terminate if it has
            current_time = time.time()
            if current_time-start_time > game_length:
               break

    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0,0,0), 264)
