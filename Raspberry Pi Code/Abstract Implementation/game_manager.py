# Abstract design for game system that is overridden for individual games
# Game system manages all of the individual player's games for all rooms

# Need to add arduino component

import time
import serial
from random import randint
import argparse

from game import Game
from light_strip import LightStrip

class GameManager:
    NUM_TARGETS_PER_ROOM = 8
    NUM_ROOMS = 4
    LED_PER_TARGET = 33

    def __init__(self, num_players):
        """Add all physical components to the game manager"""

        # Get the key starting information from the app
        # left out for now
        self.ROOMS = [0]
        self.TARGET_TIME = 5
        self.GAME_TIME = 60

        # Create and store serial access
        self.serial_connections = []
        self.serial_connections.append(serial.Serial("/dev/ttyUSB0", 9600, timeout=1))
        # self.serial_connections.append(serial.Serial("/dev/ttyUSB1", 9600, timeout=1))
        # self.serial_connections.append(serial.Serial("/dev/ttyUSB2", 9600, timeout=1))
        # self.serial_connections.append(serial.Serial("/dev/ttyUSB3", 9600, timeout=1))

        # Reset serial logs
        for i in range(0, len(self.serial_connections)):
            self.serial_connections[i].reset_input_buffer()

        # Set the number of players
        self.num_players = num_players

        # Create the object for the lightstrip
        self.lights = LightStrip()

        # Create the games
        self._games = []
        for r in range(0, len(self.ROOMS)):
            room = []
            for player in range(0, self.num_players):
                room.append(Game(self.ROOMS[r], player, self.lights))
            self._games.append(room)

        #Start the timer
        self.start_time = time.time()

        # Notifies the app that the system is starting
        print("START")
    
    def update(self, newTargetPicker):
        """Runs all game associated actions, decision making, and SSH updates (NOT DONE)"""

        target_log = []

        for i in range(0, len(self.serial_connections)):
            while(self.serial_connections[i].in_waiting > 0):
                line = int(self.serial_connections[i].readline().decode('utf-8').rstrip()) + 8 * i
                target_log.append(line)
                print(line)

        # Check all values
        for room in range(0, len(self._games)):
            game = self._games[room][0]
            if game.getTarget() in target_log:
                self.newTargetPicker(game)
                

        # Update lights
        for room in range(0, len(self._games)):
            game = self._games[room][0]

            # Update lights
            game.updateLightsCountdown()

            # Update target if all lights are out
            if game.checkCountdownEnded():
                game.setTarget(self.pickRandomTarget(room, [game.getTarget()]))
                game.resetCounter()

        # Wait
        time.sleep(self.TARGET_TIME / self.LED_PER_TARGET)

    def pickRandomTarget(self, room, exceptions=[]):
        """Pick a target from a room excluding given targets"""
        x = room*self.NUM_TARGETS_PER_ROOM + randint(0, self.NUM_TARGETS_PER_ROOM - 1)

        while x in exceptions:
            x = room*self.NUM_TARGETS_PER_ROOM + randint(0, self.NUM_TARGETS_PER_ROOM - 1)

        return x
    
    def pickNextTarget(self, game):
        game.addPoint()
        game.setTarget(self.pickRandomTarget(room, [game.getTarget()]))
        game.resetCounter()

    def timeExpired(self):
        return time.time() - self.start_time >= self.GAME_TIME

    def end(self):
        """Manages end notification and score communication via SSH and turns on end lights"""
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

        # Sends out final scores
        for game in self._games:
            game.reportScore()
        
        # Notifies the app that the system is terminated
        print("END")
