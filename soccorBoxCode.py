import time
from random import random
from random import randint
import argparse
from rpi_ws281x import *
from gpiozero import Button
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# LED Constants
LED_COUNT      = 264
LED_PIN        = 18      # GPIO pin (uses PWM)
LED_FREQ_HZ    = 800000
LED_DMA        = 10  
LED_BRIGHTNESS = 100     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False
LED_CHANNEL    = 0
LED_PER_TARGET = 33
NUM_TARGERTS = 8

# Colors
RED = Color(255, 0, 0)
GREEN = Color(0, 255, 0)
BLUE = Color(0, 0, 255)
BLACK = Color(0, 0, 0)
WHITE = Color(255, 255, 255)

# OLED STUFF
RST = None
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# Piezos
PIEZOCERAMIC_PINS = [6, 12, 13, 19, 16, 26, 20, 21] # GPIOs

# Initialize score display
oled_display = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

oled_display.begin()

oled_display.clear()
oled_display.display()

width = oled_display.width
height = oled_display.height
image = Image.new('1', (width, height))

draw = ImageDraw.Draw(image)
draw.rectangle((0,0,width,height), outline=0, fill=0)

font = ImageFont.load_default()

padding = -2
top = padding
bottom = height-padding


def colorWipe(strip, color, wait_ms, target):
    """Wipe color across display a pixel at a time. Returns 1 if the associated piezoceramic is triggered."""
    start = target*LED_PER_TARGET

    for i in range(start, start + LED_PER_TARGET):
        strip.setPixelColor(i, color)
        strip.show()

        # Delay while checking piezo
        if checkPiezoForTime(target, wait_ms / 1000):
            return 1

    return 0

def colorWipeByIndex(strip, color, wait_ms, target, index, num_simeltaneous):
    """Wipe color across display a pixel at a time with simeltaneous capability. Returns True if associated piezo is triggered"""
    i = target*LED_PER_TARGET + index

    strip.setPixelColor(i, color)
    strip.show()

    # Delay while checking piezo
    if checkPiezoForTime(target, wait_ms/(1000 * num_simeltaneous)):
        return True

    return True
	
def fillAll(strip, color, target):
    """Instantly change color of pixels on a target"""
    start = target*LED_PER_TARGET

    for i in range(start, start + LED_PER_TARGET):
        strip.setPixelColor(i, color)

    strip.show()

def resetAll(strip):
    for target in range(0, NUM_TARGERTS):
            fillAll(strip, BLACK, target)

def checkPiezoForTime(index, duration):
    """Check piezoceramic state for a set time until time expires or the piezoceramic is triggered. Returns if the piezoceramic was triggered (boolean)"""
    start_time = time.time()

    while (time.time() - start_time < duration):
        if piezoceramics[index].is_pressed:
            print("TARGET " + index + " HIT")
            return True

    return False

def limitedInput(prompt, acceptableAnswers):
    """Takes user input. Accepts predetermined answers and reasks the user for input when any other answer is given"""

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

def clearOLED():
    draw.rectangle((0,0,width,height), outline=0, fill=0)

def displayScore(num_players, scores):
    clearOLED()

    # Write two lines of text.
    for x in range(0, num_players):
        draw.text((x * 50, top),       "P" + (x + 1),  font=font, fill=255)
        draw.text((x * 50, top+8),     str(score[x]), font=font, fill=255)

    # Display image.
    oled_display.image(image)
    oled_display.display()

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
                        # Reset all targets
                        resetAll(strip)

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
                        for x in range(0, LED_PER_TARGET):
                            left_target = colorWipeByIndex(strip, RED, target_length, 3, x, 3)
                            center_target = colorWipeByIndex(strip, GREEN, target_length, 4, x, 3)
                            right_target = colorWipeByIndex(strip, BLUE, target_length, 5, x, 3)

                            # Check results
                            if left_target:
                                if designated_color == RED:
                                    score[0] += 1
                                break
                            elif center_target:
                                if designated_color == GREEN:
                                    score[0] += 1
                                break
                            elif right_target:
                                if designated_color == BLUE:
                                    score[0] += 1
                                break

                        reset[0] = True

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
                        # targets[0] = 0

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
                p1 = colorWipeByIndex(strip, BLACK, target_length, targets[0], index[0], 2)
                p2 = colorWipeByIndex(strip, BLACK, target_length, targets[1], index[0], 2)

                index[0] += 1

                if index[0] >= LED_PER_TARGET:
                    reset[0] = True

                if p1:
                    score[0] += 1
                    reset[0] = True
                
                if p2:
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
                colorWipeByIndex(strip, BLACK, target_length, targets[0], index[0], 2)
                colorWipeByIndex(strip, BLACK, target_length, targets[1], index[1], 2)

                index[0] += 1
                index[1] += 1

                for x in range(0, 2):
                    if piezoceramics[targets[x]].is_pressed:
                        score[x] += 1
                        reset[x] = True
                    elif index[x] >= NUM_TARGERTS:
                        reset[x] = True
            
            # Display score
            displayScore(num_players, score)

            # Terminate when time expires
            current_time = time.time()
            if current_time-start_time > game_length:
                for target in range(0, NUM_TARGERTS):
                    fillAll(strip, BLACK, target)
                    clearOLED()
                break

    except KeyboardInterrupt:
        resetAll(strip)
        clearOLED()