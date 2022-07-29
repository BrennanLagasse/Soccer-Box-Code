# Stores all attributes and methods for the light strip

from rpi_ws281x import *

class LightStrip:
    LED_PIN = 18
    LED_FREQ_HZ = 800000
    LED_DMA = 10
    LED_BRIGHTNESS = 100
    LED_INVERT = False
    LED_CHANNEL = 0
    LED_PER_TARGET = 33
    NUM_TARGETS_ROOM = 8
    NUM_ROOMS = 4
    LED_COUNT = LED_PER_TARGET * NUM_TARGETS_ROOM * NUM_ROOMS

    BLACK = Color(0, 0, 0)


    def __init__(self):
        """Create a new light strip object with the specs of the four box system"""
        self.strip = Adafruit_NeoPixel(self.LED_COUNT, self.LED_PIN, self.LED_FREQ_HZ, self.LED_DMA, self.LED_INVERT, self.LED_BRIGHTNESS, self.LED_CHANNEL)
        self.strip.begin()

    def color_wipe(self, room, target, index):
        """Erase color at the given index"""
        i = (room*self.NUM_TARGETS_ROOM + target)*self.LED_PER_TARGET + index
        self.strip.setPixelColor(i, self.BLACK)
        self.strip.show()

    def fill_target(self, color, room, target):
        """Instantly change color of all lights in target range"""
        start = (room*self.NUM_TARGETS_ROOM + target)*self.LED_PER_TARGET
        for i in range(start, start + self.LED_PER_TARGET):
            self.strip.setPixelColor(i, color)
        self.strip.show()

    def fill_room(self, color, room):
        """Instantly change color of all lights in a room"""
        start = room*self.NUM_TARGETS_ROOM*self.LED_PER_TARGET
        for i in range(start, start + self.LED_PER_TARGET*self.NUM_TARGETS_ROOM):
            self.strip.setPixelColor(i, color)
        self.strip.show()

    def reset_all(self):
        """Reset all of the LEDs in the smart box"""
        for target in range(0, self.NUM_TARGETS):
                self.fill_all(self.strip, self.BLACK, target)
