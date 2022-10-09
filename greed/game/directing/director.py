from calendar import c
from game.casting.gem import Gem
from game.casting.rock import Rock
from game.shared.color import Color
from game.shared.point import Point
from random import randint


FRAME_RATE = 12
CELL_SIZE = 15
COLS = 60
FONT_SIZE = 15
GEM_CHR_CODE = 164
ROCK_CHR_CODE = 214
DEFAULT_START = 10
DEFAULT_SPAWN_CHANCE = 20
SPAWN_COOLDOWN = 5
MAX_FALLING = 40


class Director:
    """A person who directs the game. 
    
    The responsibility of a Director is to control the sequence of play.

    Attributes:
        _keyboard_service (KeyboardService): For getting directional input.
        _video_service (VideoService): For providing video output.
    """

    def __init__(self, keyboard_service, video_service, cast):
        """Constructs a new Director using the specified keyboard and video services.
        
        Args:
            keyboard_service (KeyboardService): An instance of KeyboardService.
            video_service (VideoService): An instance of VideoService.
        """
        self._keyboard_service = keyboard_service
        self._video_service = video_service
        self._cast = cast
        self._timer = SPAWN_COOLDOWN * FRAME_RATE

        for n in range(DEFAULT_START):
            self._try_spawning()            
        
    def start_game(self):
        """Starts the game using the given cast. Runs the main game loop.

        Args:
            cast (Cast): The cast of actors.
        """
        self._video_service.open_window()
        while self._video_service.is_window_open():
            self._get_inputs(self._cast)
            self._do_updates(self._cast)
            self._do_outputs(self._cast)
        self._video_service.close_window()

    def _get_inputs(self, cast):
        """Gets directional input from the keyboard and applies it to the robot.
        
        Args:
            cast (Cast): The cast of actors.
        """
        player = cast.get_first_actor("player")
        velocity = self._keyboard_service.get_direction()
        player.set_velocity(velocity)        

    def _do_updates(self, cast):
        """Updates the robot's position and resolves any collisions with artifacts.
        
        Args:
            cast (Cast): The cast of actors.
        """
        banner = cast.get_first_actor("banners")
        player = cast.get_first_actor("player")
        falling = cast.get_actors("falling")

        max_x = self._video_service.get_width()
        max_y = self._video_service.get_height()
        player.move_next(max_x)
        
        for falls in falling:
            if falls.is_alive():
                falls.move_next(max_y)                    
                if player.get_position().equals(falls.get_position()):
                    points = falls.get_points()
                    banner.add_points(points)
                    falls.kill()
                    falling.remove(falls)

        if len(falling) < MAX_FALLING:
            self._try_spawning()        
        
    def _do_outputs(self, cast):
        """Draws the actors on the screen.
        
        Args:
            cast (Cast): The cast of actors.
        """
        self._video_service.clear_buffer()
        actors = cast.get_all_actors()
        self._video_service.draw_actors(actors)
        self._video_service.flush_buffer()

    def _try_spawning(self):
        if self._timer >= 0:
            roll = randint(1, 100)
            if roll <= DEFAULT_SPAWN_CHANCE:
                x = randint(1, COLS - 1)
                position = Point(x, 0)
                position = position.scale(CELL_SIZE)

                r = randint(0, 255)
                g = randint(0, 255)
                b = randint(0, 255)
                color = Color(r, g, b)

                if roll % 2 == 0:
                    text = chr(ROCK_CHR_CODE)
                    falling = Rock()

                else:
                    text = chr(GEM_CHR_CODE)
                    falling = Gem()

                falling.set_text(text)
                falling.set_font_size(FONT_SIZE)
                falling.set_color(color)
                falling.set_position(position)
                self._cast.add_actor("falling", falling)
        
            self._timer -= 1

        else:
            self._timer = SPAWN_COOLDOWN * FRAME_RATE