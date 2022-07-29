# Most recent code as of 6/29/2022

import time
import serial
from random import random
from random import randint
import argparse

# Lights
from rpi_ws281x import *



# Global variables
# Previous is the log of targets that have been sent to the arduino
prev = []

# Tnitialize and start RGB lights



# Check Log
def check_log(target, duration):
    """Check log for duration between light changes"""
    if target in prev:
        return True

    # Clear the log as the data has been seen while checking 2 targets by now
    prev.clear()

    start_time = time.time()

    while (time.time() - start_time < duration):
        # Check if the value is being sent + update log
        if (arduino.inWaiting() > 0): 
            # Get new information
            line = arduino.readline()

            # Remove data after reading
            arduino.flushInput()

            # Convert to integer
            try:
                val = int(line)
                print(val)
            except:
                # Silently removes value
                print("WARNING: Bad input from arduino")

            # Check if target is in new info
            if(val == target):
                return True

            # Add info to temporary log
            if not (val in prev):
                prev.append(val)

    return False
	
def fill_all(strip, color, target):
    """Instantly change color of pixels in target range"""
    start = target*LED_PER_TARGET
    for i in range(start, start + LED_PER_TARGET):
        strip.setPixelColor(i, color)
    strip.show()

def limited_input(prompt, acceptableAnswers):
    """Takes user input and reasks the user when an unacceptable answer is given"""
    while True:
        response = input(prompt)
        if response in acceptableAnswers:
            return response
        else:
            print("Invalid input.")
    
def generate_color():
    x = randint(1, 3)
    if x == 1:
        return RED
    elif x == 2:
        return GREEN
    return BLUE

def pick_target(exceptions=[]):
    """Pick a target excluding given targets"""
    x = randint(0, NUM_TARGETS - 1)
    while x in exceptions:
        x = randint(0, NUM_TARGETS - 1)
    
    return x

def reset_all(strip):
    """Reset all of the LEDs in the smart box"""
    for target in range(0, NUM_TARGETS):
            fill_all(strip, BLACK, target)

class LightStrip:
    LED_PIN = 18
    LED_COUNT = 264
    LED_FREQ_HZ = 800000
    LED_DMA = 10
    LED_BRIGHTNESS = 100
    LED_INVERT = False
    LED_CHANNEL = 0
    LED_PER_TARGET = 33
    NUM_TARGETS = 8


    def __init__(self):
        self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        self.strip.begin()

    # Define functions which animate LEDs in various ways.
    def color_wipe(strip, color, target, index):
        """Erase color across a target one pixel at a time"""

        i = target*LED_PER_TARGET + index

        strip.setPixelColor(i, BLACK)
        strip.show()
