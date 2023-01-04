# Stores all attributes and methods for the light strip

from rpi_ws281x import *

class LightStrip:
    LED_PIN = 18
    LED_FREQ_HZ = 800000
    LED_DMA = 10
    LED_BRIGHTNESS = 50
    LED_INVERT = False
    LED_CHANNEL = 0
    LED_PER_TARGET = 33
    NUM_TARGETS_ROOM = 8
    NUM_ROOMS = 2
    LED_COUNT = LED_PER_TARGET * NUM_TARGETS_ROOM * NUM_ROOMS

    BLACK = Color(0, 0, 0)


    def __init__(self):
        """Create a new light strip object with the specs of the four box system"""
        self.strip = Adafruit_NeoPixel(self.LED_COUNT, self.LED_PIN, self.LED_FREQ_HZ, self.LED_DMA, self.LED_INVERT, self.LED_BRIGHTNESS, self.LED_CHANNEL)
        self.strip.begin()

    def colorWipe(self, targets, index):
        """Turn off last light of given index at all listed targets (simultaneous is key to prevent repeat calls to show)"""
        for i in range(0, len(targets)):
            i = index + targets[i]*self.LED_PER_TARGET
            self.strip.setPixelColor(i, self.BLACK)
        self.strip.show()

    def fillTarget(self, color, target):
        """Instantly change color of all lights in target range. This is where rerouting occurs"""

        # Rerouting algorithm
        if(target >= 8 and target % 8 != 0):
            target = target + 8 - 2*(target % 8)

        start = target*self.LED_PER_TARGET
        for i in range(start, start + self.LED_PER_TARGET):
            self.strip.setPixelColor(i, color)
        self.strip.show()

    def fillRemainingTarget(self, color, target, index):
        """Instantly change all remaining lights on a target to a different color"""
        start = target*self.LED_PER_TARGET + index
        for i in range(start, start + self.LED_PER_TARGET  - index):
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

    def fillTargetSegment(self, color, target, segment):
        """Fill a segment of a target: (0) first ten (1) next thirteen (2) last ten"""
        start = target*self.LED_PER_TARGET

        if(segment == 0):
            for i in range(start, start + 10):
                self.strip.setPixelColor(i, color)
        if(segment == 1):
            for i in range(start + 10, start + 23):
                self.strip.setPixelColor(i, color)
        if(segment == 2):
            for i in range(start + 23, start + 33):
                self.strip.setPixelColor(i, color)
        self.strip.show()
