import time
import serial
from random import random
from random import randint
import argparse

# Lights
from rpi_ws281x import *

# LED info
LED_PIN = 18
LED_COUNT      = 264
LED_FREQ_HZ    = 800000
LED_DMA        = 10
LED_BRIGHTNESS = 100
LED_INVERT     = False
LED_CHANNEL    = 0
LED_PER_TARGET = 33
NUM_TARGETS = 8

# Colors
RED = Color(255, 0, 0)
GREEN = Color(0, 255, 0)
BLUE = Color(0, 0, 255)
BLACK = Color(0, 0, 0)
WHITE = Color(255, 255, 255)
ORANGE = Color(253, 88, 0)

TEAM_COLORS = [RED, BLUE]
TEAM_NEXT_COLORS = [ORANGE, GREEN]

# Games
GAMES = {
    "1" : " (1) ONE PLAYER - STANDARD \n",
    "2" : " (2) ONE PLAYER - FRONT ONLY \n",
    "3" : " (3) ONE PLAYER - GLANCING GOALS \n",
    "4" : " (4) ONE PLAYER - PREPERATION PLAYS \n",
    "5" : " (5) TWO PLAYER - SYNCHRONOUS \n",
    "6" : " (6) TWO PLAYER - ASYNCHRONOUS \n",
    "7" : " (7) TWO PLAYER - PREPERATION PLAYS \n"
}

GAME_DATA = [
    # num_players | front_five  | competitive | glancing_goals | preperation | path
    [1,            False,        False,        False,           False       ], # 1
    [1,            True,         False,        False,           False       ], # 2
    [1,            False,        False,        True,            False       ], # 3
    [1,            False,        False,        False,           True        ], # 4
    [2,            False,        True,         False,           False       ], # 5
    [2,            False,        False,        False,           False       ], # 6
    [2,            False,        False,        False,           True        ]  # 7
]

# Global variables
score = [0, 0]
prev = []

# Tnitialize and start RGB lights
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()


# Define functions which animate LEDs in various ways.
def color_wipe(strip, color, target, index, wait_ms, num_simeltaneous):
    """Wipe color across display a pixel at a time"""
    i = target*LED_PER_TARGET + index

    strip.setPixelColor(i, color)
    strip.show()

    
    time.sleep(wait_ms/(1000 * num_simeltaneous) )

# Check Log
def check_log(target):
    """Check log for duration between light changes"""
    if target in prev:
        return True

    # Clear the log as the data has been seen twice by now
    prev.clear()

    # Check if the value is being sent + update log
    while (arduino.inWaiting()>0): 
        # Get new information
        val = int(arduino.readline())

        # Print value
        print(str(val) + " hit")

        # Check if target is in new info
        if(val == target):
            return True

        # Add info to temporary log
        prev.append(val)

        # Remove data after reading
        arduino.flushInput()

    return False
	
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

def resetAll(strip):
    """Reset all of the LEDs in the smart box"""
    for target in range(0, NUM_TARGETS):
            fillAll(strip, BLACK, target)


def game_from_input():
    n = int(limitedInput("Select a game mode:\n" + GAMES["1"] + GAMES["2"] + GAMES["3"] + GAMES["4"] + GAMES["5"] + GAMES["6"] + GAMES["7"], 
            ["1", "2", "3", "4", "5", "6", "7"])) - 1

    target_length = int(input("Time in seconds to hit target:\n")) / LED_PER_TARGET*1000 

    game_length = int(input("Time in seconds of game:\n"))

    return Game(target_length, game_length, GAME_DATA[n][0], GAME_DATA[n][1], GAME_DATA[n][2], GAME_DATA[n][3], GAME_DATA[n][4])

class Game:
    def __init__(self, target_length, game_length, num_players=1, front_five=False, competitive=False, glancing_goals=False, preperation=False):
        # Set input variables
        self.target_length = target_length
        self.game_length = game_length
        self.num_players = num_players
        self.front_five = front_five
        self.competitive = competitive
        self.glancing_goals = glancing_goals
        self.preperation = preperation

        # Create generic variables
        self.start_time = time.time()
        self.targets = [0]
        self.next_targets = [0]
        self.index = [0, 0]
        self.exit = False

        # Pick initial target(s)
        if self.num_players > 1:
            self.targets.append(0)
        if self.preperation:
            self.next_targets[0] = pick_target()
            self.next_targets.append(pick_target([self.next_targets[0]]))

        for i in range(0, self.num_players):
            self.reset(i)
        

    def update(self):
        # Update with general function
        if (self.glancing_goals):
            self.glancing_goals_update()
        else:
            self.standard_update()

        # Terminate when time expires
        current_time = time.time()
        if current_time - self.start_time > self.game_length:
            resetAll(strip)
            self.exit = True

    def standard_update(self):
        for i in range(0, self.num_players):
            # Update display
            color_wipe(strip, BLACK, self.targets[i], self.index[i], self.target_length, self.num_players)

            # Check for score
            check = check_log(self.targets[i])

            if(check):
                print("Score!")
                score[i] += 1
                if(self.competitive):
                    self.reset(0)
                    self.reset(1)
                else:
                    self.reset(i)
                continue


            self.index[i] += 1

            if(self.index[i] >= LED_PER_TARGET):
                self.reset(i)
                print(self.targets[i])
                print("\n")

    def glancing_goals_update(self):
        print("not done yet")
        self.exit = True

    def reset(self, player):
        # Reset previous target
        fillAll(strip, BLACK, self.targets[player])

        # Pick new target
        if(self.front_five):
            self.targets[player] = randint(2, 6)
        elif(self.preperation):
            self.targets[player] = self.next_targets[player]
            if(self.num_players == 1):
                self.next_targets[player] = pick_target([self.targets[player]])
            else:
                self.next_targets[player] = pick_target([self.targets[0], self.targets[1], self.next_targets[0], self.next_targets[1]])
        else:
            if(self.num_players == 1):
                self.targets[player] = pick_target()
            else:
                self.targets[player] = pick_target(self.targets)

        # Color new target
        fillAll(strip, TEAM_COLORS[player], self.targets[player])

        # Color next target (if preperation)
        if self.preperation:
            fillAll(strip, TEAM_NEXT_COLORS[player], self.next_targets[player])

        self.index[player] = 0


if __name__ == '__main__':
    print('Running. Press CTRL-C to exit.')

    with serial.Serial("/dev/ttyACM0", 9600, timeout=1) as arduino:
        # Wait for serial to open
        time.sleep(0.1) 

        # Ensure serial connection before starting the game
        if arduino.isOpen():
            print("{} connected!".format(arduino.port))

            # Process arguments
            parser = argparse.ArgumentParser()
            parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
            args = parser.parse_args()
            
            # User Input
            game = game_from_input()

            try:
                while True:
                    game.update()
                    
                    if (game.exit):
                        print("GAME OVER\n")
                        for i in range(0, game.num_players):
                            print("Player " + str(i + 1) + " score: " + str(score[i]))
                        break

            except KeyboardInterrupt:
                for target in range(0, NUM_TARGETS - 1):
                    resetAll(strip)