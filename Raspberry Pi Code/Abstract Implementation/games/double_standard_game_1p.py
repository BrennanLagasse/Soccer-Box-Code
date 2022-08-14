# Recreates original code for original game with LightStrip and Game classes

from game_manager import GameManager

NUM_PLAYERS = 1

class DoubleStandardOnePlayerGame(GameManager):
    """A standard game where each target must be hit twice"""
    def __init__(self):
        super().__init__(NUM_PLAYERS)

        # Pick initial target
        for room in range(0, len(self._games)):
            self._games[room][0].setTarget(super().pickRandomTarget(room))
    
    def update(self):
        super().update(game_manager.pickNextTarget)
    
    def pickNextTarget(self, game, score):
        if score:
            if game.getFlag() == 1:
                game.addPoint()
                game.resetTarget(game.getTarget())
                game.setTarget(self.pickRandomTarget(game.getRoom(), [game.getTarget()]))
                game.resetCounter()
                game.setFlag(0)
            else:
                game.colorTarget(game.color_alternate, game.getTarget())
                game.setFlag(1)
        

if __name__ == '__main__':
    print('Running. Press CTRL-C to exit.')

    game_manager = DoubleStandardOnePlayerGame()

    try:
        while not game_manager.timeExpired():
            # WIP Read values from arduinos and store in log. Build in wait here
            game_manager.update()
        game_manager.end()

    except KeyboardInterrupt:
        print("Interrupt")
        game_manager.end()
