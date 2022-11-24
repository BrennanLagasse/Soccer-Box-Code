# Recreates original code for original game with LightStrip and Game classes
# Description: 2 targets light up and must hit both before time expires (first hit turns off that target, second hit switches to next target), set time, set target time
# Initially, both targets are red. When one is hit, the remaining target turns yellow

from game_manager import GameManager

NUM_PLAYERS = 1

class OnePlayerBothTargetGame(GameManager):
    """Standard game except player must hit both targets that appear in the time frame"""
    def __init__(self):
        super().__init__(NUM_PLAYERS)

        # Pick initial targets
        for room in self._games:
            room[0].setTarget(super().pickRandomTarget(room[0].getRoom()))
            room[0].setNextTarget(super().pickRandomTarget(room[0].getRoom(), {room[0].getTarget()}))
            room[0].colorTargetAlternate()
    
    def update(self):
        super().update(self.checkTargets, self.pickNextTarget, self.lightUpdate)

    def checkTargets(self, target_log, newTargetPicker):
        """Checks and manages target hits. Looks at both target options"""
        # The flag is used to track which target is hit: 
        # 0 means no hit, 1 means target 1 is hit, and 2 means target 2 is hit
        for room in range(0, len(self._games)):
            for i in range(self.num_players):
                game = self._games[room][i]
                if game.getTarget() in target_log:
                    game.resetTarget(game.getTarget())
                    if(game.getFlag() == 2):
                        # Both targets were hit, reset
                        newTargetPicker(game, True, None)
                        game.setFlag(0)
                    else:
                        # One target was hit, update flag and change other target color
                        game.setFlag(1)
                        game.colorRemainingTarget(game.getNextTarget(), game.color_alternate)
                if game.getNextTarget() in target_log:
                    game.resetTarget(game.getNextTarget())
                    if(game.getFlag() == 1):
                        # Both targets were hit, reset
                        newTargetPicker(game, True, None)
                        game.setFlag(0)
                    else:
                        # One target was hit, update flag and change other target color
                        game.setFlag(2)
                        game.colorRemainingTarget(game.getTarget(), game.color_alternate)

    def pickNextTarget(self, game, score, other_target):
        if(score):
            self.addPoints(game)

        # Reset Targets
        game.resetTarget(game.getTarget())
        game.resetTarget(game.getNextTarget())

        # Pick new targets
        exceptions = []
        exceptions.append(game.getTarget())
        exceptions.append(game.getNextTarget())
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

    game_manager = OnePlayerBothTargetGame()

    try:
        while not game_manager.timeExpired():
            # WIP Read values from arduinos and store in log. Build in wait here
            game_manager.update()
        game_manager.end()

    except KeyboardInterrupt:
        print("Interrupt")
        game_manager.end()
