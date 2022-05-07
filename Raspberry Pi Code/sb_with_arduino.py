# Most recent code as of 11/19/2021

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
    "7" : " (7) TWO PLAYER - PREPERATION PLAYS \n",
    "8" : " (8) CUSTOM PATHS \n"
}

GAME_DATA = [
    # num_players | front_five  | competitive | glancing_goals | preperation | path
    [1,            False,        False,        False,           False       ], # 1
    [1,            True,         False,        False,           False       ], # 2
    [1,            False,        False,        True,            False       ], # 3
    [1,            False,        False,        False,           True        ], # 4
    [2,            False,        True,         False,           False       ], # 5
    [2,            False,        False,        False,           False       ], # 6
    [2,            False,        False,        False,           True        ],  # 7
    [1,            False,        False,        False,           False       ] # 8
]

GAME_PATH_DATA = [
    # num_reps | reflect | path targets .... 
    [3,         True,      [0, 1, 2, 3, 4, 5, 6, 7]],
    [5,         False,     [0, 1, 7, 2, 6, 3, 5, 4]]
]

# Global variables
# Previous is the log of targets that have been sent to the arduino
prev = []

# Tnitialize and start RGB lights
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()


# Define functions which animate LEDs in various ways.
def color_wipe(strip, color, target, index):
    """Wipe color across display a pixel at a time"""
    i = target*LED_PER_TARGET + index

    strip.setPixelColor(i, color)
    strip.show()

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
                val = -1

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


def game_from_input():
    n = int(limited_input("Select a game mode:\n" + GAMES["1"] + GAMES["2"] + GAMES["3"] + GAMES["4"] + GAMES["5"] + GAMES["6"] + GAMES["7"] + GAMES["8"], 
            ["1", "2", "3", "4", "5", "6", "7", "8"])) - 1

    path_data = []

    if (n == 7):
        path_data = GAME_PATH_DATA[int(input("Path number: \n"))]

    target_length = float(input("Time in seconds to hit target:\n")) / LED_PER_TARGET*1000 

    game_length = float(input("Time in seconds of game:\n"))

    return Game(target_length, game_length, GAME_DATA[n][0], GAME_DATA[n][1], GAME_DATA[n][2], GAME_DATA[n][3], GAME_DATA[n][4], path_data)

class Game:
    def __init__(self, target_length, game_length, num_players=1, front_five=False, competitive=False, 
    glancing_goals=False, preperation=False, use_path=False, path=[]):

        # Set input variables
        self.target_length = target_length
        self.game_length = game_length
        self.num_players = num_players
        self.front_five = front_five
        self.competitive = competitive
        self.glancing_goals = glancing_goals
        self.preperation = preperation
        self.use_path = use_path
        if(use_path):
            self.path_repeats = path[0]
            self.path_reverse = path[1]
            self.path = path[2]
            self.path_direction = 1
            self.path_position = 0

        # Create generic variables
        self.start_time = time.time()

        # Current targets that the player needs to hit
        self.targets = [0]

        self.next_targets = [0]
        self.index = [0, 0]
        self.score = [0, 0]
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
            reset_all(strip)
            self.exit = True

    def standard_update(self):
        for i in range(0, self.num_players):
            # Update display
            color_wipe(strip, BLACK, self.targets[i], self.index[i])

            # Check for score for duration of wait time
            duration = self.target_length/(1000 * self.num_players)
            check = check_log(self.targets[i], duration)

            if(check):
                print("Score!")
                self.score[i] += 1
                if(self.competitive):
                    self.reset(0)
                    self.reset(1)
                else:
                    self.reset(i)

            self.index[i] += 1

            if(self.index[i] >= LED_PER_TARGET):
                self.reset(i)

    def glancing_goals_update(self):
        # Set initial target
        initial_target = 0
        fill_all(strip, WHITE, initial_target)

        # Wait until initial target hit
        check = check_log(initial_target, time.time() - self.start_time - self.game_length )

        if check:
            # Array of colors for far targets
            colors = [RED, GREEN, BLUE]

            random.shuffle(colors)

            # Color front targets
            for i in range(0, 2):
                fill_all(strip, colors[i], i + 3)

            # Pick designated target
            target_index = randint(3, 5)

            # Color a back target with the indicator color
            fill_all(strip, colors[target_index - 3], 1 + 6 * randint(0, 1))

            # Check for score
            duration = self.target_length/(1000 * 3)
            check2 = check_log(self.targets[i], duration)

            if(check2):
                self.score[0] += 1
            
            reset_all(strip)


    def reset(self, player):
        # Reset previous target
        fill_all(strip, BLACK, self.targets[player])

        # Pick new target
        if(self.use_path):
            self.path_position += self.path_direction

            if(self.path_position >= len(self.path)):
                if(self.path_reverse):
                    self.path_position -= 1
                    self.path_direction = -1
                else:
                    self.path_position = 0
                self.path_repeats -= 1
            elif(self.path_position < 0):
                self.path_position = 0
                self.path_direction = 1
                self.path_repeats -= 1
            
            if(self.path_repeats < 0):
                self.exit = True

            self.targets[player] = self.path[self.path_position]
        elif(self.front_five):
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
        if self.num_players == 1:
            # fill_all(strip, generate_color(), self.targets[player])
            print("")
        else:
            # fill_all(strip, TEAM_COLORS[player], self.targets[player])
            print("")

        # Color next target (if preperation)
        if self.preperation:
            fill_all(strip, TEAM_NEXT_COLORS[player], self.next_targets[player])

        self.index[player] = 0



if __name__ == '__main__':
    print('Running. Press CTRL-C to exit.')

    # All working. Use this as test
    # for i in range(0, 8):
        # fill_all(strip, BLUE, i)
        # time.sleep(1)
        # reset_all(strip)

    # "/dev/ttyACM0" at home
    with serial.Serial("/dev/ttyUSB0", 9600, timeout=1) as arduino:
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
                            print("Player " + str(i + 1) + " score: " + str(game.score[i]))
                        break

            except KeyboardInterrupt:
                for target in range(0, NUM_TARGETS - 1):
                    reset_all(strip)
