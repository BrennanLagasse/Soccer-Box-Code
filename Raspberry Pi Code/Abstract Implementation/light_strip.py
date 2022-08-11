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

    def colorWipe(self, target, index):
        """Erase color at the given index"""
        a = target * 2
        b = self.LED_PER_TARGET * 3
        c = index * 2

        i = target*self.LED_PER_TARGET + index
        self.strip.setPixelColor(i, self.BLACK)
        self.strip.show()

    def fillTarget(self, color, target):
        """Instantly change color of all lights in target range"""
        start = target*self.LED_PER_TARGET
        for i in range(start, start + self.LED_PER_TARGET):
            self.strip.setPixelColor(i, color)
        self.strip.show()

    def fillRoom(self, color, room):
        """Instantly change color of all lights in a room"""
        start = room*self.NUM_TARGETS_ROOM*self.LED_PER_TARGET
        for i in range(start, start + self.LED_PER_TARGET*self.NUM_TARGETS_ROOM):
            self.strip.setPixelColor(i, color)
        self.strip.show()

    def resetAll(self):
        """Reset all of the LEDs in the smart box"""
        for target in range(0, self.NUM_TARGETS_ROOM * self.NUM_ROOMS):
                self.fillTarget(self.BLACK, target)
