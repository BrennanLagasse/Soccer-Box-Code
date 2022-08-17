# Tests lights by turning on targets one at a time
import time
from rpi_ws281x import *

from light_strip import LightStrip

BLUE = Color(0, 0, 255)
BLACK = Color(0, 0, 0)
ORANGE = Color(253, 88, 0)

NUM_TARGETS_PER_ROOM = 8
NUM_ROOMS = 1

# Tnitialize and start RGB lights
lights = LightStrip()

if __name__ == '__main__':
    print("START")

    # All working. Use this as test
    for target in range(0, NUM_ROOMS*NUM_TARGETS_PER_ROOM):
        lights.fillTarget(ORANGE, target)
        time.sleep(0.75)
        lights.fillTarget(BLACK, target)

    print("END")
