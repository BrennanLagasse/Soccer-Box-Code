# Class that stores all data and functionality related to a single player

import time
import serial
from random import random
from random import randint
import argparse

from rpi_ws281x import *

from light_strip.py import LightStrip;

class Game:

    LED_PER_TARGET = 33
    NUM_TARGETS = 8

    RED = Color(255, 0, 0)
    GREEN = Color(0, 255, 0)
    BLUE = Color(0, 0, 255)
    WHITE = Color(255, 255, 255)
    ORANGE = Color(253, 88, 0)

    def __init__(self, room_number, player_number, lights):
        """Creates a new manager for a single player"""
        self.room = room_number
        self.player = player_number
        self.score = 0
        self.lights = lights
        self.light_index = 0
        self.target = 0
        self.next_target = 0

        if self.player == 0:
            self.color_primary = self.RED
            self.color_alternate = self.ORANGE
        else:
            self.color_primary = self.BLUE
            self.color_alternate = self.GREEN

    def setTarget(self, target):
        self.target = target
    
    def getTarget(self):
        return self.target

    def setNextTarget(self, next_target):
        self.next_target = next_target

    def getNextTarget(self):
        return self.next_target

    def addPoint(self):
        self.score += 1

    def getScore(self):
        return self.score
    
    def checkCountdownEnded(self):
        """Returns if the light countdown has ended"""
        return self.i >= self.LED_PER_TARGET

    def resetCounter(self):
        self.light_index = 0

    def updateLightsCountdown(self):
        """Turns off the next light in sequence on the target"""
        self.lights.color_wipe(self.room, self.target, self.light_index)
        self.light_index += 1

    def colorTarget(self, color, target):
        """Lights up a target in the given color"""
        self.lights.fill_target(color, target)

    def colorTargetPrimary(self, target):
        """Lights up a target in the primary theme color"""
        self.lights.fill_target(self.color_primary, target) 

    def colorTargetAlternate(self, target):
        """Lights up a target in the alternate theme color"""
        self.lights.fill_target(self.color_alternate, target)

    def startWinnerLights(self):
        """Turns on all of the lights in the player's color"""
        self.lights.fill_room(self.color_primary, self.room)
