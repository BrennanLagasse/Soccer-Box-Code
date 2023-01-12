# Tests lights by turning on targets one at a time
import time
from rpi_ws281x import *

from light_strip import LightStrip

BLACK = Color(0,0,0)


RED = Color(255, 0, 0)
ORANGE = Color(210, 30, 0)
YELLOW = Color(255, 155, 0)
GREEN = Color(0, 255, 0)
BLUE = Color(0, 0, 255)
PURPLE = Color(125,51, 230)
PINK = Color(255, 80, 40)
WHITE = Color(255, 255, 255)

NUM_TARGETS_PER_ROOM = 8
NUM_ROOMS = 3

# Tnitialize and start RGB lights
lights = LightStrip()

if __name__ == '__main__':
    print("START")

    colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, PINK, WHITE]

    # Good: Red, Yellow Green, Blue, White
    # Bad: Orange, Purple, Pink

    # All working. Use this as test
    for i in range(0, 8):
        lights.fillTarget(colors[i], i)

    print("END")
