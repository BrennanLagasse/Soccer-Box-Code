# Recreates original code for original game with LightStrip and Game classes

from game_manager import GameManager

NUM_PLAYERS = 1

class OnePlayerNextGame(GameManager):
    """Standard game where the next target is shown"""
    def __init__(self):
        super().__init__(NUM_PLAYERS)

        # Pick initial targets
        for room in range(0, len(self._games)):
            game = self._games[room][0]
            game.setTarget(super().pickRandomTarget(room))
            game.setNextTarget(super().pickRandomTarget(room, {game.getTarget()}))
    
    def update(self):
        super().update(self.checkTargets, self.pickNextTarget, self.standardLightUpdate)

    def pickNextTarget(self, game, score, other_game=None):
        if score:
            game.addPoint()
        game.resetTarget(game.getTarget())
        game.setTarget(game.getNextTarget())
        game.setNextTarget(self.pickRandomTarget(game.getRoom(), [game.getTarget()]))
        game.colorTargetAlternate()
        game.resetCounter()


if __name__ == '__main__':
    print('Running. Press CTRL-C to exit.')

    game_manager = OnePlayerNextGame()

    try:
        while not game_manager.timeExpired():
            # WIP Read values from arduinos and store in log. Build in wait here
            game_manager.update()
        game_manager.end()

    except KeyboardInterrupt:
        print("Interrupt")
        game_manager.end()
