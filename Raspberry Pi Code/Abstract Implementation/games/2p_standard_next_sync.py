# Recreates original code for original game with LightStrip and Game classes

from game_manager import GameManager

NUM_PLAYERS = 2

class TwoPlayerNextSyncGame(GameManager):
    """Two player syncronous game where next target for each player is shown"""
    def __init__(self):
        super().__init__(NUM_PLAYERS)

        exceptions = []

        # Pick initial targets
        for room in self._games:
            for game in room:
                target = super().pickRandomTarget(room, exceptions)
                exceptions.append(target)
                game.setTarget()
                next_target = super().pickRandomTarget(room, exceptions)
                exceptions.append(next_target)
                game.setNextTarget(next_target)
    
    def update(self):
        super().update(self.checkTargets, self.pickNextTarget, self.standardLightUpdate)

    def pickNextTarget(self, game, score, other_game):
        if score:
            game.addPoint()

        # Reset targets
        game.resetTarget(game.getTarget())
        other_game.resetTarget(other_game.getTarget())

        # Set the target to the next target
        game.setTarget(game.getNextTarget())
        other_game.getTarget(other_game.getNextTarget())

        # Pick next target
        game.setNextTarget(self.pickRandomTarget(game.getRoom(), [game.getTarget(), other_game.getTarget()]))
        other_game.setNextTarget(self.pickRandomTarget(other_game.getRoom(), [game.getTarget(), other_game.getTarget(), other_game.getNextTarget()]))

        # Color next target
        game.colorTargetAlternate()
        other_game.colorTargetAlternate()

        # Reset counter
        game.resetCounter()
        other_game.resetCounter()


if __name__ == '__main__':
    print('Running. Press CTRL-C to exit.')

    game_manager = TwoPlayerNextSyncGame()

    try:
        while not game_manager.timeExpired():
            # WIP Read values from arduinos and store in log. Build in wait here
            game_manager.update()
        game_manager.end()

    except KeyboardInterrupt:
        print("Interrupt")
        game_manager.end()
