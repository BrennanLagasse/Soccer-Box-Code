# Recreates original code for original game with LightStrip and Game classes
# Description:
# Targets 4-6 and 2 or 8 light up
# Player must hit the front target (4-6) that matches the light in the back (2 or 8) that turns on in the same color
# Only 2 OR 8 turns on

from game_manager import GameManager
from random import randint

NUM_PLAYERS = 1

class ShoulderCheckBasicGame(GameManager):
    """Standard Game"""
    def __init__(self):
        super().__init__(NUM_PLAYERS)

        # Pick initial target
        for room in range(0, len(self._games)):
            for game in room:
                # Set the actual target as a front target 4-6 (targets[3:5])
                game.setTarget(super().pickRandomTarget(room, [0, 1, 2, 6, 7]))

                colors = [game.ORANGE, game.YELLOW, game.GREEN, game.BLUE, game.PURPLE, game.PINK, game.WHITE]

                # Color front targets randomly 4-6 (targets[3:5]) 
                # and color one back target the same color 2 or 8 (targets[1] or targets[7])
                for i in range(room * 8 + 3, room * 8 + 6):
                    color = colors.pop(randint(0, len(colors) - 1))
                    game.colorTarget(color, i)

                    if i == game.getTarget():
                        # Turn on either target 1 (0) or 8 (7) to match
                        game.colorTarget(color, 1 + 6*randint(0,1))

        
    def update(self):
        super().update(self.checkTargets, self.pickNextTarget, self.standardLightUpdate)

    def randomColors(self, game):
        colors = [game.ORANGE, game.YELLOW, game.GREEN, game.BLUE, game.PURPLE, game.PINK, game.WHITE]

        # Color front targets randomly 4-6 (targets[3:5]) 
        # and color one back target the same color 2 or 8 (targets[1] or targets[7])
        for i in range(game.getRoom() * 8 + 3, game.getRoom() * 8 + 6):
            color = colors.pop(randint(0, len(colors) - 1))
            game.colorTarget(color, i)

            if i == game.getTarget():
                # Turn on either target 1 (0) or 8 (7) to match
                game.colorTarget(color, 1 + 6*randint(0,1))

if __name__ == '__main__':
    print('Running. Press CTRL-C to exit.')

    game_manager = ShoulderCheckBasicGame()

    try:
        while not game_manager.timeExpired():
            # WIP Read values from arduinos and store in log. Build in wait here
            game_manager.update()
        game_manager.end()

    except KeyboardInterrupt:
        print("Interrupt")
        game_manager.end()
