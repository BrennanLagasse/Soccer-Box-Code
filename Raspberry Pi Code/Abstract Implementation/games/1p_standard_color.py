# Recreates original code for original game with LightStrip and Game classes
# Description: all targets light up but only one is the correct red target, set time, set target time

from game_manager import GameManager
from random import randint

NUM_PLAYERS = 1

class StandardOnePlayerColorGame(GameManager):

    """Standard Game"""
    def __init__(self):
        super().__init__(NUM_PLAYERS)

        # Pick initial targets
        for room in range(0, len(self._games)):
            game = self._games[room][0]

            # Pick the first target and color red
            game.setTarget(super().pickRandomTarget(room))

            # Color the rest of the targets at random
            self.randomColors(game)
    
    def update(self):
        super().update(self.checkTargets, self.pickNextTarget, self.lightUpdate)

    def pickNextTarget(self, game, score, other_game):
        """Selects new targets and updates score based on boolean score"""
        if score:
            self.addPoints(game)
        
        # Color new target
        game.setTarget(self.pickRandomTarget(game.getRoom(), [game.getTarget()]))

        # Color all other targets
        self.randomColors(game)

        game.resetCounter()

    def lightUpdate(self, newTargetPicker):
        """Does countdown for target in each game and resets when timer ends. Override for other"""
        for room in self._games:
            for game in room:
                # Update lights
                start = game.getRoom()*8
                targets = [i + start for i in range(0,8)]
                game.updateLightsCountdownAlt(targets)

                # Update target if all lights are out
                if game.checkCountdownEnded():
                    newTargetPicker(game, False, None)

    def randomColors(self, game):
        colors = [game.ORANGE, game.YELLOW, game.GREEN, game.BLUE, game.PURPLE, game.PINK, game.WHITE]

        for i in range(game.getRoom() * 8, game.getRoom() * 8 + super().NUM_TARGETS_PER_ROOM):
                if not (i == game.getTarget()):
                    game.colorTarget(colors.pop(randint(0, len(colors) - 1)), i)


if __name__ == '__main__':
    print('Running. Press CTRL-C to exit.')

    game_manager = StandardOnePlayerColorGame()

    try:
        while not game_manager.timeExpired():
            # WIP Read values from arduinos and store in log. Build in wait here
            game_manager.update()
        game_manager.end()

    except KeyboardInterrupt:
        print("Interrupt")
        game_manager.end()
