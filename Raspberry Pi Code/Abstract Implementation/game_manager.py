# Abstract design for game system that is overridden for individual games
# Game system manages all of the individual player's games for all rooms

# Need to add arduino component

import time
import serial
from random import random
from random import randint
import argparse

from game.py import Game
from light_strip.py import LightStrip

#Temporarily hold inputs as global variables
ROOMS = [1, 2, 4]
TARGET_TIME = 5
GAME_TIME = 60

class GameManager:

    NUM_TARGETS_PER_ROOM = 8
    NUM_ROOMS = 4

    def __init__(self, num_players):
        """Add all physical components to the game manager"""

        self.num_players = num_players

        # Create the object for the lightstrip
        self.lights = LightStrip()

        # Create the games
        self._games = []
        for room in range (0, len(ROOMS)):
            for player in range(0, self.num_players):
                self._games[room][player] = Game(room, player, self.lights)

        #Start the timer
        self.start_time = time.time()
    
    def update(self):
        """Runs all game associated actions, decision making, and SSH updates (NOT DONE)"""
        print("Update")

    def pickRandomTarget(self, room, exceptions=[]):
        """Pick a target from a room excluding given targets"""
        x = room*self.NUM_TARGETS_PER_ROOM + randint(0, self.NUM_TARGETS_PER_ROOM - 1)
        while x in exceptions:
            x = room*self.NUM_TARGETS_PER_ROOM + randint(0, self.NUM_TARGETS_PER_ROOM - 1)

    def timeExpired(self):
        return time.time() - self.start_time >= GAME_TIME

    def end(self):
        """Lights up the winner boxes (DONE) and sends out final information via SSH (NOT DONE)"""
        if self.num_players == 1:
            max_score = 0
            best_player = []

            # Find all players with the highest score
            for r in range(0, len(self._games)):
                score = self._games[r][0].getScore()

                if (score > max_score):
                    best_player = [r]
                    max_score = score
                elif (score == max_score):
                    best_player.append(r)

            for r in range(0, len(best_player)):
                self._games[r][0].startWinnerLights()
        else:
            # Find the winner of each game, no lights if no winner
            for r in range(0, len(self._games)):
                score1 = self._games[r][0].getScore()
                score2 = self._games[r][1].getScore()

                if (score1 > score2):
                    self._games[r][0].startWinnerLights()
                elif (score2 > score1):
                    self._games[r][1].startWinnerLights()