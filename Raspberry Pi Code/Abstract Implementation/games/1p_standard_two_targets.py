# Recreates original code for original game with LightStrip and Game classes

from game_manager import GameManager

NUM_PLAYERS = 1

class StandardOnePlayerGame(GameManager):
    """Standard game except player can choose from either of two targets (Still need to check on second target)"""
    def __init__(self):
        super().__init__(NUM_PLAYERS)

        # Pick initial targets
        for room in range(0, len(self._games)):
            self._games[room][0].setTarget(super().pickRandomTarget(room))
            self._games[room][0].setNextTarget(super().pickRandomTarget(room, {self._games.getTarget()}))
    
    def update(self):
        super().update(self.pickNextTarget)

    def pickNextTarget(self, game, score, other_target):
        if(score):
            game.addPoint()
        exceptions = []
        exceptions.append(game.getTarget())
        exceptions.append(game.getNextTarget())
        game.resetTarget(game.getTarget())
        game.resetTarget(game.getNextTarget())
        game.setTarget(super().pickRandomTarget(game.getRoom(), exceptions))
        exceptions.append(game.getTarget())
        game.setNextTarget(super().pickRandomTarget(game.getRoom(), exceptions))
        game.colorTarget(game.color_primary, game.getNextTarget())
        game.resetCounter()




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
