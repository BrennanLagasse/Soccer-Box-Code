# Recreates original code for original game with LightStrip and Game classes

import time
import serial
from random import random
from random import randint
import argparse

from light_strip.py import LightStrip
from game.py import Game
from game_manager.py import GameManager

NUM_PLAYERS = 1


class StandardOnePlayerGame(GameManager):
    def __init__(self):
        super().__init__(self, NUM_PLAYERS)

        # Pick initial targets
        for room in range(0, len(self._games)):
            self._games[room][0].setTarget(super.pickRandomTarget(room))
    
    def update(self):
        super().update(self)

        # Find all targets to check
        targets = []

        for room in range(0, len(self._games)):
            targets.append(self._games[room][0].getTarget())

        # WIP Read values from arduinos and store in log. Build in wait here
        target_log = []

        # Check all values
        for room in range(0, len(self._games)):
            game = self.games[room][0]
            if game.getTarget() in target_log:
                game.addPoint()
                game.setTarget(super().pickRandomTarget(room, [game.getTarget()]))
                game.resetCounter()


        # Update lights
        for room in range(0, len(self._games)):
            game = self._games[room][0]

            # Update lights
            game.updateLightsCountdown()

            # Update target if all lights are out
            if game.checkCountdownEnded():
                game.setTarget(super().pickRandomTarget(room, [game.getTarget()]))
                game.resetCounter()


if __name__ == '__main__':
    print('Running. Press CTRL-C to exit.')

    game_manager = StandardOnePlayerGame()

    try:
        while not game_manager.timeExpired():
            game_manager.update()
        game_manager.end()

    except KeyboardInterrupt:
        for target in range(0, NUM_TARGETS - 1):
            reset_all(strip)