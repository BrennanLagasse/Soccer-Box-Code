# Recreates original code for original game with LightStrip and Game classes

from game_manager import GameManager
from random import randint

NUM_PLAYERS = 1

class StandardOnePlayerGame(GameManager):
    """Standard Game"""
    def __init__(self):
        super().__init__(NUM_PLAYERS)

        # Pick initial target
        for room in range(0, len(self._games)):
            self._games[room][0].setTarget(super().pickRandomTarget(room, [0, 1, 2, 6, 7]))
    
    def update(self):
        super().update(self.checkTargets, self.pickNextTarget, self.standardLightUpdate)

    def randomColors(self, game):
        colors = [game.ORANGE, game.YELLOW, game.GREEN, game.BLUE, game.PURPLE, game.PINK, game.WHITE]

        # Color front targets randomly (2, 3, 4, 5, 6) and color one back target the same color (1, 7)
        for i in range(game.getRoom() * 8 + 2, game.getRoom() * 8 + 7):
            color = colors.pop(randint(0, len(colors) - 1))
            game.colorTarget(color, i)

            if i == game.getTarget():
                game.colorTarget(color, 1 + 6*randint(0,1))

if __name__ == '__main__':
    print('Running. Press CTRL-C to exit.')

    game_manager = StandardOnePlayerGame()

    try:
        while not game_manager.timeExpired():
            # WIP Read values from arduinos and store in log. Build in wait here
            game_manager.update()
        game_manager.end()

    except KeyboardInterrupt:
        print("Interrupt")
        game_manager.end()
