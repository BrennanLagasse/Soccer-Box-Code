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

        if self.player == 1:
            self.color = self.RED
        else:
            self.color = self.BLUE

    def updateLightsCountdown(self, target):
        """Turns off the next light in sequence on the target"""
        self.lights.color_wipe(self.room, target, self.light_index)
        self.light_index += 1

    def checkCountdownEnded(self):
        """Returns if the light countdown has ended"""
        return self.i >= self.LED_PER_TARGET

    def colorTarget(self, color, target):
        """Lights up a target in the given color"""
        self.lights.fill_target(color, self.room, target)

    def startWinnerLights(self):
        """Turns on all of the lights in the player's color"""
        self.lights.fill_room(self.color, self.room)
