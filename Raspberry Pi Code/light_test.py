# Most recent code as of 11/19/2021

# Lights
import time
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

# Tnitialize and start RGB lights
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()


# Define functions which animate LEDs in various ways.
def color_wipe(strip, color, target, index):
    """Wipe color across display a pixel at a time"""
    i = target*LED_PER_TARGET + index

    strip.setPixelColor(i, color)
    strip.show()
	
def fill_all(strip, color, target):
    """Instantly change color of pixels in target range"""
    start = target*LED_PER_TARGET
    for i in range(start, start + LED_PER_TARGET):
        strip.setPixelColor(i, color)
    strip.show()

def reset_all(strip):
    """Reset all of the LEDs in the smart box"""
    for target in range(0, NUM_TARGETS):
            fill_all(strip, BLACK, target)

if __name__ == '__main__':
    print('Running. Press CTRL-C to exit.')

    # All working. Use this as test
    for i in range(0, 8):
        for j in range(0,33):
            color_wipe(strip, BLUE, i, j)
            time.sleep(0.05)
        reset_all(strip)
