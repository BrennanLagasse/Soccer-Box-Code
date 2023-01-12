# Recreates original code for original game with LightStrip and Game classes
# 2 targets each (current and next), set time, set target time, 2 players

from game_manager import GameManager

NUM_PLAYERS = 2

class TwoPlayerNextAsyncGame(GameManager):
    """Two player asyncronous game where next target for each player is shown"""
    def __init__(self):
        super().__init__(NUM_PLAYERS)

        exceptions = []

        # Pick initial targets
        for room in self._games:
            for game in room:
                target = super().pickRandomTarget(game.getRoom(), exceptions)
                exceptions.append(target)
                game.setTarget(target)
                next_target = super().pickRandomTarget(game.getRoom(), exceptions)
                exceptions.append(next_target)
                game.setNextTarget(next_target)

                # Color next target
                game.colorTargetAlternate()
                game.colorTargetAlternate()
    
    def update(self):
        super().update(self.checkTargets, self.pickNextTarget, self.standardLightUpdate)

    def pickNextTarget(self, game, score, other_game):
        if score:
            self.addPoints(game)

        # Get exceptions
        exceptions = [game.getTarget(), other_game.getTarget(), game.getNextTarget(), other_game.getNextTarget()]

        # Reset targets
        game.resetTarget(game.getTarget())

        # Set the target to the next target
        game.setTarget(game.getNextTarget())

        # Pick next target
        game.setNextTarget(self.pickRandomTarget(game.getRoom(), exceptions))
        
        # Color next target
        game.colorTargetAlternate()

        # Reset counter
        game.resetCounter()


if __name__ == '__main__':
    print('Running. Press CTRL-C to exit.')

    game_manager = TwoPlayerNextAsyncGame()

    try:
        while not game_manager.timeExpired():
            # WIP Read values from arduinos and store in log. Build in wait here
            game_manager.update()
        game_manager.end()

    except KeyboardInterrupt:
        print("Interrupt")
        game_manager.end()
