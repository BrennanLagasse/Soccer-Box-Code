# Recreates original code for original game with LightStrip and Game classes

from game_manager import GameManager

NUM_PLAYERS = 2

class ThreeGoalsFirstGame(GameManager):
    """Game where player must hit all of opponents three targets before theirs are hit to win"""
    def __init__(self):
        super().__init__(NUM_PLAYERS)

        self.player1_targets = [0, 1, 7]
        self.player2_targets = [2, 4, 6]

        # Color targets to start
        for room in range(0, len(self._games)):
            game1 = self._games[room][0]
            
            for i in self.player1_targets:
                target = room * 8 + i
                game1.colorTarget(game1.color_primary, target)
                game1.extras.append(target)

            game2 = self._games[room][1]

            for i in self.player2_targets:
                target = room * 8 + i
                game2.colorTarget(game2.color_primary, target)
                game2.extras.append(target)
    
    def update(self):
        super().update(self.checkTargets, self.pickNextTarget, self.standardLightUpdate)

    def checkTargets(self, target_log, newTargetPicker):
        """Checks all active targets for a player"""
        for room in self._games:
            for game in room:
                for target in game.extras:
                    if target in target_log:
                        game.addPoints(1)
                        game.resetTarget(target)
                        game.extras.remove(target)
                if len(game.extras) == 0:
                    self.end()

    def standardLightUpdate(self, newTargetPicker):
        """Do Nothing"""

if __name__ == '__main__':
    print('Running. Press CTRL-C to exit.')

    game_manager = ThreeGoalsFirstGame()

    try:
        while not (game_manager.timeExpired() or game_manager.gameOver()):
            # WIP Read values from arduinos and store in log. Build in wait here
            game_manager.update()
        game_manager.end()

    except KeyboardInterrupt:
        print("Interrupt")
        game_manager.end()
