from game.casting.falling import Falling


class Gem(Falling):
    def __init__(self):
        super().__init__()
        self._points = 1

    def get_points(self):
        return self._points