# Class that stores all data and functionality related to a single player

from rpi_ws281x import *
import time

class Game:

    LED_PER_TARGET = 33
    NUM_TARGETS = 8

    BLACK = Color(0,0,0)
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

    def getRoom(self):
        return self.room

    def setTarget(self, target):
        self.target = target
        self.colorTargetPrimary()
    
    def getTarget(self):
        return self.target

    def setNextTarget(self, next_target):
        self.next_target = next_target

    def getNextTarget(self):
        return self.next_target

    def addPoint(self):
        self.score += 1
        self.reportScore()

    def getScore(self):
        return self.score

    def reportScore(self):
        """Prints out a string formatted for the app to read as [s] [room] [player] [score]"""
        print("s " + str(self.room) + " " + str(self.player) + " " + str(self.score))
    
    def checkCountdownEnded(self):
        """Returns if the light countdown has ended"""
        return self.light_index >= self.LED_PER_TARGET

    def resetCounter(self):
        self.light_index = 0

    def updateLightsCountdown(self):
        """Turns off the next light in sequence on the target"""
        self.lights.colorWipe(self.target, self.light_index)
        self.light_index += 1

    def colorTarget(self, color, target):
        """Lights up a target in the given color"""
        self.lights.fillTarget(color, target)

    def resetTarget(self, target):
        """Sets a target to black"""
        self.lights.fillTarget(self.BLACK, target)

    def colorTargetPrimary(self):
        """Lights up a target in the primary theme color"""
        self.lights.fillTarget(self.color_primary, self.target) 

    def colorTargetAlternate(self):
        """Lights up a target in the alternate theme color"""
        self.lights.fillTarget(self.color_alternate, self.next_target)

    def startWinnerLights(self):
        """Flashes all of the lights in the player's color twice then turns them off"""
        for i in range(2):
            self.lights.fillRoom(self.color_primary, self.room)
            time.sleep(0.5)
            self.lights.resetAll()
            time.sleep(0.5)
        
