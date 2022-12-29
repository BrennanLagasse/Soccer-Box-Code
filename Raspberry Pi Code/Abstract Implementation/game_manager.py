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

        self.complete = False

        # Format: Number of rooms, r1, ... , rn, target time, game time
        a = input("Number of Rooms: ")
        num_rooms = int(a)
        self.ROOMS = []
        for i in range(num_rooms):
            a = input("Room " + str(i) + ": ")
            self.ROOMS.append(int(a))
        a = input("Target Time: ")
        self.TARGET_TIME = int(a)
        a = input("Game Time: ")
        self.GAME_TIME = int(a)

        # Create and store serial access
        self.serial_connections = []
        self.serial_connections.append(serial.Serial("/dev/ttyUSB0", 9600, timeout=1))
        self.serial_connections.append(serial.Serial("/dev/ttyUSB1", 9600, timeout=1))
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
    
    def update(self, checkTargets, newTargetPicker, lightsUpdate):
        """Runs all game associated actions, decision making, and SSH updates"""

        # Get log of targets that where hit
        target_log = self.getTargetLog()

        # Check for valid hits and respond
        checkTargets(target_log, newTargetPicker)   

        # Update lights and reset expired targets
        lightsUpdate(newTargetPicker)

        # Wait
        time.sleep(self.TARGET_TIME / self.LED_PER_TARGET)

    def getTargetLog(self):
        """Get a list of all the targets to check for"""
        target_log = []

        for i in range(0, len(self.serial_connections)):
            while(self.serial_connections[i].in_waiting > 0):
                line = int(self.serial_connections[i].readline().decode('utf-8').rstrip()) + 8 * i
                target_log.append(line)

        return target_log

    def addPoints(self, game, points=1):
        """Adds a point to the given game and notifies the nano to update the scoreboard"""
        game.addPoints(points)
        score_message = "P" + str(game.getPlayer()) + "S" + str(game.getScore())
        self.writeToArduino(game.getRoom(), score_message)

    def writeToArduino(self, room, message):
        """Send a message to the arduino"""
        formatted_message = str(message) + "\n"
        self.serial_connections[room].write(formatted_message.encode('utf-8'))

    def checkTargets(self, target_log, newTargetPicker):
        """Checks and manages target hits. Override when player has multiple active targets"""
        for room in range(0, len(self._games)):
            for i in range(self.num_players):
                game = self._games[room][i]
                if game.getTarget() in target_log:
                    if (self.num_players == 1):
                        newTargetPicker(game, True, None)
                    else:
                        newTargetPicker(game, True, self._games[room][(i+1) % 2])
                    

    def standardLightUpdate(self, newTargetPicker):
        """Does countdown for target in each game and resets when timer ends. Override for other"""
        for room in self._games:
            for game in room:
                # Update lights
                game.updateLightsCountdown()

                # Update target if all lights are out
                if game.checkCountdownEnded():
                    if(self.num_players == 1):
                        newTargetPicker(game, False, None)
                    else:
                        newTargetPicker(game, False, self._games[game.getRoom()][(game.getPlayer() + 1) % 2])


    def pickRandomTarget(self, room, exceptions=[]):
        """Pick a target from a room excluding given targets. Room is an integer, exceptions is a list"""
        x = room*self.NUM_TARGETS_PER_ROOM + randint(0, self.NUM_TARGETS_PER_ROOM - 1)

        while x in exceptions:
            x = room*self.NUM_TARGETS_PER_ROOM + randint(0, self.NUM_TARGETS_PER_ROOM - 1)

        return x
    
    def pickNextTarget(self, game, score, other_game):
        """Selects new targets and updates score based on boolean score"""
        if score:
            self.addPoints(game)
        game.resetTarget(game.getTarget())
        game.setTarget(self.pickRandomTarget(game.getRoom(), [game.getTarget()]))
        game.resetCounter()

    def pickTwoDoubleTargets(self, game, other_game):
        """Sets up a two player game where each player has two targets that are both active"""
        games = [game, other_game]
        exceptions = []

        for g in games:
            g.setTarget(self.pickRandomTarget(g.getRoom()))
            exceptions.append(g.getTarget())
            g.setNextTarget(self.pickRandomTarget(g.getRoom(), exceptions))
            g.colorTarget(g.color_primary, g.getNextTarget())
            exceptions.append(g.getNextTarget())

    def timeExpired(self):
        return time.time() - self.start_time >= self.GAME_TIME

    def setGameOver(self):
        """Triggers the kill switch for the game"""
        self.complete = True

    def gameOver(self):
        """Returns a boolean that indicates if the program is over"""
        return self.complete

    def end(self, room=0):
        """Manages end notification and score communication via SSH and turns on end lights"""
        # Case: Single Player.
        if self.num_players == 1:
            max_score = 0
            best_player = []

            # Find all players with the highest score
            for r in self.ROOMS:
                score = self._games[r][0].getScore()

                if (score > max_score):
                    best_player = [r]
                    max_score = score
                elif (score == max_score):
                    best_player.append(r)

            for r in range(0, len(best_player)):
                self._games[r][0].startWinnerLights()

        # Case: Two Player.
        else:
            # Find the winner of each game, once in each color if there is no winner
            for r in self.ROOMS:
                score1 = self._games[r][0].getScore()
                score2 = self._games[r][1].getScore()

                if (score1 > score2):
                    self._games[r][0].startWinnerLights()
                elif (score2 > score1):
                    self._games[r][1].startWinnerLights()
                else:
                    self._games[r][0].startTieLights()

        # Sends out final scores
        for room in self._games:
            for game in room:
                game.reportScore()
        
        # Notifies the app that the system is terminated
        print("END")