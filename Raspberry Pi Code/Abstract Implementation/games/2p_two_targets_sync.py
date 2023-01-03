# Recreates original code for original game with LightStrip and Game classes

from game_manager import GameManager
import time

NUM_PLAYERS = 2

class TwoPlayerTwoTargetSyncGame(GameManager):
    """Standard game except player can choose from either of two targets"""
    def __init__(self):
        super().__init__(NUM_PLAYERS)
        
        # Pick initial targets
        for room in self._games:
            super().pickTwoDoubleTargets(room[0], room[1])
    
    def update(self):
        super().update(self.checkTargets, self.pickNextTarget, self.lightUpdate)

    def checkTargets(self, target_log, newTargetPicker):
        """Checks and manages target hits. Looks at both target options"""
        for room in range(0, len(self._games)):
            for i in range(self.num_players):
                game = self._games[room][i]
                if (game.getTarget() in target_log) or (game.getNextTarget() in target_log):
                    newTargetPicker(game, True, self._games[room][(i+1) % 2])

    def pickNextTarget(self, game, score, other_game):
        if(score):
            self.addPoints(game)

        games = [game, other_game]

        # Reset Targets
        for g in games:
            g.resetTarget(g.getTarget())
            g.resetTarget(g.getNextTarget())

        # Pause to prevent rereading
        time.sleep(0.35)

        # Pick new targets
        exceptions = []
        
        for g in games:
            g.setTarget(super().pickRandomTarget(g.getRoom(), exceptions))
            exceptions.append(g.getTarget())
            g.setNextTarget(super().pickRandomTarget(g.getRoom(), exceptions))
            exceptions.append(g.getNextTarget())

        # Color new targets and reset counter
        for g in games:
            g.colorTarget(g.color_primary, g.getNextTarget())
            g.resetCounter()

    def lightUpdate(self, newTargetPicker):
        """Does countdown for target in each game and resets when timer ends. Override for other"""
        for room in self._games:
            for i in range(self.num_players):
                game = room[i]

                # Update lights
                targets = [game.getTarget(), game.getNextTarget()]
                game.updateLightsCountdownAlt(targets)

                # Update target if all lights are out
                if game.checkCountdownEnded():
                    newTargetPicker(game, False, self._games[game.getRoom()][(i+1) % 2])


if __name__ == '__main__':
    print('Running. Press CTRL-C to exit.')

    game_manager = TwoPlayerTwoTargetSyncGame()

    try:
        while not game_manager.timeExpired():
            # WIP Read values from arduinos and store in log. Build in wait here
            game_manager.update()
        game_manager.end()

    except KeyboardInterrupt:
        print("Interrupt")
        game_manager.end()
