# Recreates original code for original game with LightStrip and Game classes
# Description: only uses targets 3 to 7, 1 target, set time, set target time

from game_manager import GameManager

NUM_PLAYERS = 1

class RondoGame(GameManager):
    """Standard Game"""
    def __init__(self):
        super().__init__(NUM_PLAYERS)

        # Pick initial targets
        for room in range(0, len(self._games)):
            self._games[room][0].setTarget(super().pickRandomTarget(room, [0, 1, 7]))
    
    def update(self):
        super().update(self.checkTargets, self.pickNextTarget, self.standardLightUpdate)

    def pickNextTarget(self, game, score, other_game):
        """Selects new targets and updates score based on boolean score"""
        if score:
            self.addPoints(game)
        game.resetTarget(game.getTarget())
        game.setTarget(self.pickRandomTarget(game.getRoom(), [0, 1, 7]))
        game.resetCounter()
    

if __name__ == '__main__':
    print('Running. Press CTRL-C to exit.')

    game_manager = RondoGame()

    try:
        while not game_manager.timeExpired():
            # WIP Read values from arduinos and store in log. Build in wait here
            game_manager.update()
        game_manager.end()

    except KeyboardInterrupt:
        print("Interrupt")
        game_manager.end()
