from data.states.game.components.particles_draw import ParticlesDraw
from data.helpers.board_helpers import coords_to_screen_pos
from data.managers.animation import animation
from data.utils.constants import ShaderType
from data.managers.window import window
from data.utils.enums import Colour

class CaptureDraw:
    def __init__(self, board_position, board_size):
        self._board_position = board_position
        self._square_size = board_size[0] / 10
        self._particles_draw = ParticlesDraw()

    def add_capture(self, piece, colour, rotation, piece_coords, sphinx_coords, active_colour, particles=True, shake=True):
        if particles:
            self._particles_draw.add_captured_piece(
                piece,
                colour,
                rotation,
                coords_to_screen_pos(piece_coords, self._board_position, self._square_size),
                self._square_size
            )
            self._particles_draw.add_sparks(
                3,
                (255, 0, 0) if active_colour == Colour.RED else (0, 0, 255),
                coords_to_screen_pos(sphinx_coords, self._board_position, self._square_size)
            )

        if shake:
            window.set_effect(ShaderType.SHAKE)
            animation.set_timer(500, lambda: window.clear_effect(ShaderType.SHAKE))

    def draw(self, screen):
        self._particles_draw.draw(screen)

    def update(self):
        self._particles_draw.update()

    def handle_resize(self, board_position, board_size):
        self._board_position = board_position
        self._square_size = board_size[0] / 10