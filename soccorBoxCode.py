# General
import time
from random import random
from random import randint
import argparse

# Lights
from rpi_ws281x import *

# Piezoceramics
from gpiozero import Button

# OLED
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# LED strip configuration:
LED_COUNT      = 264
LED_PIN        = 18      # GPIO pin (uses PWM)
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 100     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Piezoceramic GPIO Ports (not default numbering)
PIEZOCERAMIC_PINS = [6, 12, 13, 19, 16, 26, 20, 21]

# Other Constants
LED_PER_TARGET = 33
NUM_TARGERTS = 8

# Colors
RED = Color(255, 0, 0)
GREEN = Color(0, 255, 0)
BLUE = Color(0, 0, 255)
BLACK = Color(0, 0, 0)
WHITE = Color(255, 255, 255)

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms, target):
    """Wipe color across display a pixel at a time"""
    start = target*LED_PER_TARGET

    for i in range(start, start + LED_PER_TARGET):
        strip.setPixelColor(i, color)
        strip.show()


        time_start = time.time()

        # Continuously check piezoceramic between lights
        while (time.time() - time_start < wait_ms/1000):
            if piezoceramics[target].is_pressed:
                print("TARGET HIT :)")
                return 1

    return 0

def colorWipeByIndex(strip, color, wait_ms, target, index):
    """Wipe color across display a pixel at a time with simeltaneous capability"""
    i = target*LED_PER_TARGET + index

    strip.setPixelColor(i, color)
    strip.show()

    if piezoceramics[target].is_pressed:
        print("score")
        return 1

    time.sleep(wait_ms/2000) # 2 running simeltaneously

    return 0
	
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


def generateColor():
    """Generates a random color (currently red, green, or blue)"""
    x = randint(1, 3)

    if x == 1:
        return RED
    elif x == 2:
        return GREEN
    
    return BLUE

def pickTargetExcept(exception):
    """Returns random number not equal to the exception"""
    x = randint(1, NUM_TARGERTS) - 1

    while x == exception:
        x = randint(1, NUM_TARGERTS) - 1
    
    return x

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
    piezoceramics = [] 
    
    # New Piezoceramic setup (when added)
    for x in range(0, NUM_TARGERTS):
        piezoceramics.append(Button(PIEZOCERAMIC_PINS[x]))

    # Termination Condition
    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    # User input
    game_mode = limitedInput("Select a game mode:\n (A) ONE PLAYER, ALL GOALS \n (B) ONE PLAYER, FRONT GOALS \n (C) ONE PLAYER, FRONT GOALS OVER THE SHOULDER \n (D) TWO PLAYER, SYNCHRONOUS \n (E) TWO PLAYER, ASYNCHRONOUS", 
    ["a", "b", "c", "d", "e"])

    # Default game variables
    num_players = 1
    frontFive = False
    competitive = True
    over_shoulder = False

    if (game_mode == "b"):
        frontFive = True
    elif (game_mode == "c"):
        over_shoulder = True
    elif (game_mode == "d"):
        num_players = 2
        competitive = False
    else:
        num_players = 2

    target_length = int(input("Time in seconds to hit target:\n")) / LED_PER_TARGET*1000 

    game_length = int(input("Time in seconds of game:\n"))

    start_time = time.time()


    try:
        # Initialize Game Variables
        score = [0, 0] # score[0] = p1 score, score[1] = p2 score
        targets = [0] # target[0] = p1 target, target[1] = p2 target (if applicable)
        index = [0, 0] # used for simeltaneous targets
        reset = [False, False] # Used to determine if targets need to be reset with interative

        # Pick initial target(s)
        if (frontFive):
            targets[0] = randint(2, 6)
        else:
            targets[0] = randint(1, NUM_TARGERTS) - 1

        if num_players == 2:
            targets.append(pickTargetExcept(targets[0]))

        # Repeating portion of the game
        while True:
            if num_players == 1:
                if over_shoulder:
                    if reset[0] == True:
                        # Color center target white
                        fillAll(strip, WHITE, 4)

                        # Wait until target is hit
                        while (not piezoceramics[4].is_pressed):
                            time.wait(.01)

                        # Reset target
                        fillAll(strip, BLACK, 4)

                        # Move on
                        reset[0] = False
                    else:
                        # Pick designated color
                        designated_color = generateColor()

                        # Fill in either back side target with that color (the other is blank)
                        fillAll(strip, designated_color, 1 + 6 * randint(0, 1))

                        # Fill in the front targets and wipe
                        print("NOT DONE YET")
                        


                else:
                    # Color designated target
                    fillAll(strip, generateColor(), targets[0])

                    # Wipe target, note hits, manage exit, and update score
                    score[0] += colorWipe(strip, BLACK, target_length, targets[0])

                    fillAll(strip, BLACK, targets[0])

                    if(frontFive):
                        targets[0] = randint(2,6)
                    else:
                        targets[0] = randint(0, NUM_TARGERTS - 1)
                        # targets[0] = 7

            elif competitive:

                if reset[0]:
                    # Reset previous targets
                    fillAll(strip, BLACK, targets[0])
                    fillAll(strip, BLACK, targets[1])

                    # Pick new targets
                    targets[0] = randint(0, NUM_TARGERTS - 1)
                    targets[1] = pickTargetExcept(targets[0])

                    # Color p1 target red, p2 target blue
                    fillAll(strip, RED, targets[0])
                    fillAll(strip, BLUE, targets[1])

                    # Reset index
                    index[0] = 0

                    # Reset complete
                    reset[0] = False

                # Wipe target, note hits, manage exit, and update score
                colorWipeByIndex(strip, BLACK, target_length, targets[0], index[0])
                colorWipeByIndex(strip, BLACK, target_length, targets[1], index[0])

                index[0] += 1

                if index[0] >= LED_PER_TARGET:
                    reset[0] = True


                if piezoceramics[targets[0]].is_pressed:
                    score[0] += 1
                    reset[0] = True
                
                if piezoceramics[targets[1]].is_pressed:
                    score[1] += 1
                    reset[0] = True

            else:
                if reset[0]:
                    # Reset previous target
                    fillAll(strip, BLACK, targets[0])

                    # Pick new target
                    targets[0] = pickTargetExcept(targets[1])

                    # Color p1 target red
                    fillAll(strip, RED, targets[0])

                    # Reset index
                    index[0] = 0

                    # Reset done
                    reset[0] = False
                
                if reset[1]:
                    # Reset previous target
                    fillAll(strip, BLACK, targets[1])

                    # Pick new target
                    targets[0] = pickTargetExcept(targets[0])

                    # Color p1 target red
                    fillAll(strip, RED, targets[1])

                    # Reset index
                    index[1] = 0

                    # Reset done
                    reset[1] = False

                # Wipe target, note hits, manage exit, and update score
                colorWipeByIndex(strip, BLACK, target_length, targets[0], index[0])
                colorWipeByIndex(strip, BLACK, target_length, targets[1], index[1])

                index[0] += 1
                index[1] += 1

                for x in range(0, 2):
                    if piezoceramics[targets[x]].is_pressed:
                        score[x] += 1
                        reset[x] = True
                    elif index[x] >= NUM_TARGERTS:
                        reset[x] = True
                
            # Terminate when time expires
            current_time = time.time()
            if current_time-start_time > game_length:
                for target in range(0, NUM_TARGERTS):
                    fillAll(strip, BLACK, target)
                break

    except KeyboardInterrupt:
        for target in range(0, NUM_TARGERTS):
            fillAll(strip, BLACK, target)