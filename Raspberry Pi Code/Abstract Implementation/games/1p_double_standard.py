# Double Standard Game – 1 target (must be hit twice), set time, set target time 

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
        super().update(self.checkTargets, self.pickNextTarget, self.standardLightUpdate)
    
    def pickNextTarget(self, game, score, other_game):
        if score:
            if game.getFlag() == 1:
                self.addPoints(game)
                game.resetTarget(game.getTarget())
                game.setTarget(self.pickRandomTarget(game.getRoom(), [game.getTarget()]))
                game.resetCounter()
                game.setFlag(0)
            else:
                game.colorRemainingTarget(game.getTarget(), game.color_alternate)
                game.setFlag(1)
        else:
            game.resetTarget(game.getTarget())
            game.setTarget(self.pickRandomTarget(game.getRoom(), [game.getTarget()]))
            game.resetCounter()
            game.setFlag(0)

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
