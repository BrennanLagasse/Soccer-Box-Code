# Recreates original code for original game with LightStrip and Game classes

from game_manager import GameManager

NUM_PLAYERS = 1

class StandardOnePlayerGame(GameManager):
    def __init__(self):
        super().__init__(NUM_PLAYERS)

        # Pick initial targets
        for room in range(0, len(self._games)):
            self._games[room][0].setTarget(super().pickRandomTarget(room))
    
    def update(self):
        super().update(game_manager.pickNextTarget)

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
