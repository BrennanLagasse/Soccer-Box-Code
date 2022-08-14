# Recreates original code for original game with LightStrip and Game classes

from game_manager import GameManager

NUM_PLAYERS = 2

class StandardTwoPlayerSyncGame(GameManager):
    """Standard Game"""
    def __init__(self):
        super().__init__(NUM_PLAYERS)

        # Pick initial targets
        for room in range(0, len(self._games)):
            self._games[room][0].setTarget(super().pickRandomTarget(room))
            self._games[room][1].setTarget(super().pickRandomTarget(room, {self._games[room][0].getTarget()}))
    
    def update(self):
        """Game iterative logic"""
        super().update(self.checkTargets, self.pickNextTarget, self.standardLightUpdate)

    def pickNextTarget(self, game, score, other_game):
        """Selects new targets and updates score based on boolean score"""
        if score:
            game.addPoint()

        # Reset Targets
        game.resetTarget(game.getTarget())
        other_game.resetTarget(other_game.getTarget())

        # Get new targets for both players
        game.setTarget(self.pickRandomTarget(game.getRoom(), {game.getTarget()}))
        other_game.setTarget(self.pickRandomTarget(game.getRoom(), {game.getTarget(), other_game.getTarget()}))

        # Reset counters
        game.resetCounter()
        other_game.resetCounter()

if __name__ == '__main__':
    print('Running. Press CTRL-C to exit.')

    game_manager = StandardTwoPlayerSyncGame()

    try:
        while not game_manager.timeExpired():
            # WIP Read values from arduinos and store in log. Build in wait here
            game_manager.update()
        game_manager.end()

    except KeyboardInterrupt:
        print("Interrupt")
        game_manager.end()
