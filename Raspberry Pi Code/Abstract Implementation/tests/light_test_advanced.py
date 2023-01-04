# Tests lights by turning on targets one at a time
import time
from rpi_ws281x import *

from light_strip import LightStrip

BLACK = Color(0,0,0)

WHITE = Color(255, 255, 255)
RED = Color(255, 0, 0)
ORANGE = Color(255, 165, 0)
YELLOW = Color(253, 88, 0)
GREEN = Color(0, 255, 0)
BLUE = Color(0, 0, 255)
PURPLE = Color(128,49,167)
PINK = Color(251, 72, 196)

NUM_TARGETS_PER_ROOM = 8
NUM_ROOMS = 3

# Tnitialize and start RGB lights
lights = LightStrip()

if __name__ == '__main__':
    print("START")

    # All working. Use this as test
    for target in range(0, NUM_ROOMS*NUM_TARGETS_PER_ROOM):
        for segment in range(0,3):
            lights.fillTargetSegment(ORANGE, target, segment)
            time.sleep(0.75)
            lights.fillTarget(BLACK, target)

    print("END")
