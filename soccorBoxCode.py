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

# Colors
RED = Color(255, 0, 0)
GREEN = Color(0, 255, 0)
BLUE = Color(0, 0, 255)
BLACK = Color(0, 0, 0)



# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms, target):
    """Wipe color across display a pixel at a time"""
    start = target*LED_PER_TARGET

    for i in range(start, start + LED_PER_TARGET):
        strip.setPixelColor(i, color)
        strip.show()

        if (piezoceramics[target]):
            return 1

        time.sleep(wait_ms/1000.0)

    return 0

def colorWipeByIndex(strip, color, wait_ms, target, index):
    """Wipe color across display a pixel at a time with simeltaneous capability"""
    i = target*LED_PER_TARGET + index

    strip.setPixelColor(i, color)
    strip.show()

    if (piezoceramics[target]):
        return 1

    time.sleep(wait_ms/1000.0)

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
    return Color(randint(100, 255), randint(100, 255), randint(100, 255))

def pickTargetExcept(exception):
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
    piezoceramics = [0, 0, 0, 0, 0, 0, 0, 0] # Array of piezocermaic objects (just 0s for now, add whatever read method later when fixed)

    

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
        # Initialize Game Variables
        score = [0, 0] # score[0] = p1 score, score[1] = p2 score
        targets = [0] # target[0] = p1 target, target[1] = p2 target (if applicable)
        index = [0, 0] # used for simeltaneous targets
        reset = []

        if num_players == 2:
            targets.append(0)
    
        # Pick initial targets
        targets[0] = randint(1, NUM_TARGERTS) - 1

        if num_players == 2:
            targets[1] = pickTargetExcept(targets[0])

        # Repeating portion of the game
        while True:
            if num_players == 1:
                # Color designated target
                fillAll(strip, generateColor, targets[0])

                # Wipe target, note hits, manage exit, and update score
                score[0] += colorWipe(strip, BLACK, target_length, targets[0])

            elif competitive:
                reset = False

                if reset:
                    # Reset previous targets
                    fillAll(strip, BLACK, targets[0])
                    fillAll(strip, BLACK, targets[1])

                    # Pick new targets
                    targets[0] = randint(0, NUM_TARGERTS - 1)
                    targets[1] = pickTargetExcept(targets[0])

                    # Color p1 target red, p2 target blue
                    fillAll(strip, RED, targets[0])
                    fillAll(strip, BLUE, targets[1])

                    # Reset complete
                    reset = False

                # Wipe target, note hits, manage exit, and update score
                colorWipeByIndex(strip, BLACK, target_length, targets[0], index[0])
                colorWipeByIndex(strip, BLACK, target_length, targets[1], index[1])

                index[0] += 1
                index[1] += 1

                if index[0] >= LED_PER_TARGET:
                    reset = True


                if piezoceramics[targets[0]]:
                    score[1] += 1
                    reset = True
                
                if piezoceramics[targets[1]]:
                    score[1] += 1
                    reset = True

            else:
                reset = [False, False]

                if reset[0]:
                    # Reset previous target
                    fillAll(strip, BLACK, targets[0])

                    # Pick new target
                    targets[0] = pickTargetExcept(targets[1])

                    # Color p1 target red
                    fillAll(strip, RED, targets[0])

                    # Reset done
                    reset[0] = False
                
                if reset[1]:
                    # Reset previous target
                    fillAll(strip, BLACK, targets[1])

                    # Pick new target
                    targets[0] = pickTargetExcept(targets[0])

                    # Color p1 target red
                    fillAll(strip, RED, targets[1])

                    # Reset done
                    reset[1] = False

                # Wipe target, note hits, manage exit, and update score
                colorWipeByIndex(strip, BLACK, target_length, targets[0], index[0])
                colorWipeByIndex(strip, BLACK, target_length, targets[1], index[1])

                index[0] += 1
                index[1] += 1

                for x in range(0, 2):
                    if piezoceramics[targets[x]]:
                        score[x] += 1
                        reset[x] = True
                    elif index[x] >= NUM_TARGERTS:
                        reset[x] = True
                
            # Terminate when time expires
            current_time = time.time()
            if current_time-start_time > game_length:
               break

    except KeyboardInterrupt:
        if args.clear:
            for target in range(0, NUM_TARGERTS):
                fillAll(strip, BLACK, target)