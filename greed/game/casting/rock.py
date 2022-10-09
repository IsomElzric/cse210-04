from game.casting.falling import Falling


class Rock(Falling):
    def __init__(self):
        super().__init__()
        self._spawn_chance = 50
        self._points = -1

    def get_points(self):
        return self._points