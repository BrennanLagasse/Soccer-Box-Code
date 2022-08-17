# Lights
from rpi_ws281x import *
import time

# LED info
LED_PIN = 18
LED_PER_TARGET = 33
NUM_TARGETS    = 2
LED_COUNT      = LED_PER_TARGET * NUM_TARGETS
LED_FREQ_HZ    = 800000
LED_DMA        = 10
LED_BRIGHTNESS = 50
LED_INVERT     = False
LED_CHANNEL    = 0

BLUE = Color(0, 0, 255)
BLACK = Color(0,0,0)


# Tnitialize and start RGB lights
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

# Turn on all the lights
for i in range(0, LED_PER_TARGET*NUM_TARGETS):
    strip.setPixelColor(i, BLUE)
    strip.show()
    time.sleep(0.01)

for i in range(0, LED_PER_TARGET*NUM_TARGETS):
    strip.setPixelColor(i, BLACK)
    strip.show()
    time.sleep(0.01)