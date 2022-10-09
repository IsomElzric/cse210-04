from game.casting.actor import Actor
from game.shared.point import Point


DEFAULT_FALL_SPEED = 5


class Falling(Actor):
    def __init__(self):
        self._spawn_chance = 25
        self._alive = True
        self._velocity = Point(0, DEFAULT_FALL_SPEED)

    def move_next(self, max_y):
        y = (self._position.get_y() + self._velocity.get_y()) % max_y
        self._position = Point(self._position.get_x(), y)

    def kill(self):
        self._text = ""
        self._alive = False

    def is_alive(self):
        return self._alive