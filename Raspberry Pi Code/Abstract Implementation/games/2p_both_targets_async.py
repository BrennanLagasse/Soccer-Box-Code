# Recreates original code for original game with LightStrip and Game classes

from game_manager import GameManager

NUM_PLAYERS = 2

class TwoPlayerBothTargetAsyncGame(GameManager):
    """Standard game except player must hit both targets that appear in the time frame"""
    def __init__(self):
        super().__init__(NUM_PLAYERS)
        super().pickTwoDoubleTargets()
    
    def update(self):
        super().update(self.checkTargets, self.pickNextTarget, self.lightUpdate)

    def checkTargets(self, target_log, newTargetPicker):
        """Checks and manages target hits. Looks at both target options"""
        for room in range(0, len(self._games)):
            for i in range(self.num_players):
                game = self._games[room][i]
                if game.getTarget() in target_log:
                    game.resetTarget(game.getTarget())
                    if(game.getFlag() == 2):
                        newTargetPicker(game, True, self._games[room][(i + 1) % 2])
                        game.setFlag(0)
                    else:
                        game.setFlag(1)
                if game.getNextTarget() in target_log:
                    game.resetTarget(game.getNextTarget())
                    if(game.getFlag() == 1):
                        newTargetPicker(game, True, self._games[room][(i + 1) % 2])
                        game.setFlag(0)
                    else:
                        game.setFlag(2)

    def pickNextTarget(self, game, score, other_game):
        if(score):
            game.addPoint()

        # Reset Targets
        game.resetTarget(game.getTarget())
        game.resetTarget(game.getNextTarget())

        # Pick new targets
        exceptions = [other_game.getTarget(), other_game.getNextTarget()]
        
        game.setTarget(super().pickRandomTarget(game.getRoom(), exceptions))
        exceptions.append(game.getTarget())
        game.setNextTarget(super().pickRandomTarget(game.getRoom(), exceptions))

        # Color new targets
        game.colorTarget(game.color_primary, game.getNextTarget())

        # Reset counter
        game.resetCounter()

    def lightUpdate(self, newTargetPicker):
        """Does countdown for target in each game and resets when timer ends. Override for other"""
        for room in self._games:
            for game in room:
                # Update lights
                game.updateLightsCountdown()
                game.updateLightsCountdownAlt(game.getNextTarget())

                # Update target if all lights are out
                if game.checkCountdownEnded():
                    newTargetPicker(game, False, None)




if __name__ == '__main__':
    print('Running. Press CTRL-C to exit.')

    game_manager = TwoPlayerBothTargetAsyncGame()

    try:
        while not game_manager.timeExpired():
            # WIP Read values from arduinos and store in log. Build in wait here
            game_manager.update()
        game_manager.end()

    except KeyboardInterrupt:
        print("Interrupt")
        game_manager.end()