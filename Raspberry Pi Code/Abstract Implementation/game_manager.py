# Abstract design for game system that is overridden for individual games

from game.py import Game

class GameManager:

    def __init__(self):
        print("start")