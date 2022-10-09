from tkinter.messagebox import RETRY
from game.casting.actor import Actor


class Banner(Actor):
    def __init__(self):
        super().__init__()
        self._points = 0

    def get_text(self):
        return self._text + str(self._points)

    def get_points(self):
        return self._points

    def set_points(self, points):
        self._points = points

    def add_points(self, points):
        self._points += points