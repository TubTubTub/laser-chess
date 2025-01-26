import pygame
from enum import IntEnum, StrEnum, auto

BG_COLOUR = (0, 0, 0)
PAUSE_COLOUR = (50, 50, 50, 200)
OVERLAY_COLOUR_LIGHT = (255, 0, 0, 128)
OVERLAY_COLOUR_DARK = (255, 0, 0, 196)
SCREEN_SIZE = (1200, 600)
# SCREEN_SIZE = (600, 600)
SCREEN_FLAGS = pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE | pygame.OPENGL
STARTING_SQUARE_SIZE = (SCREEN_SIZE[1] * 0.64) / 8 #Board height divded by 8
EMPTY_BB = 0
A_FILE_MASK = 0b11111111101111111110111111111011111111101111111110111111111011111111101111111110
J_FILE_MASK = 0b01111111110111111111011111111101111111110111111111011111111101111111110111111111
ONE_RANK_MASK = 0b11111111111111111111111111111111111111111111111111111111111111111111110000000000
EIGHT_RANK_MASK = 0b00000000001111111111111111111111111111111111111111111111111111111111111111111111
TEST_MASK = 0b00000000100000000010000000000000000000000000000000000000000001000000000100000000
GAMES_PER_PAGE = 10

class CursorMode(IntEnum):
    ARROW = auto()
    IBEAM = auto()
    OPENHAND = auto()
    CLOSEDHAND = auto()
    NO = auto()

class ShaderType(StrEnum):
    SHAKE = auto()
    BLOOM = auto()
    GRAYSCALE = auto()
    CRT = auto()
    RAYS = auto()
    
    _BASE = auto()
    _BLUR = auto()
    _HIGHLIGHT = auto()
    _CALIBRATE = auto()
    _LIGHTMAP = auto()
    _SHADOWMAP = auto()
    _OCCLUSION = auto()
    _BLEND = auto()
    _CROP = auto()

SHADER_MAP = {
    'default': [
        ShaderType.BLOOM
    ],
    'retro': [
        ShaderType.CRT
    ],
    'really_retro': [
        ShaderType.CRT,
        ShaderType.GRAYSCALE
    ],
}

class TranspositionFlag(StrEnum):
    LOWER = auto()
    EXACT = auto()
    UPPER = auto()

class Miscellaneous(StrEnum):
    PLACEHOLDER = auto()
    DRAW = auto()

class WidgetState(StrEnum):
    BASE = auto()
    HOVER = auto()
    PRESS = auto()

class StatusText(StrEnum):
    PLAYER_MOVE = auto()
    CPU_MOVE = auto()
    WIN = auto()
    DRAW = auto()

class SetupEventType(StrEnum):
    MENU_CLICK = auto()
    PICK_PIECE_CLICK = auto()
    ROTATE_PIECE_CLICK = auto()
    COPY_CLICK = auto()
    EMPTY_CLICK = auto()
    RESET_CLICK = auto()
    BLUE_START_CLICK = auto()
    RED_START_CLICK = auto()
    START_CLICK = auto()
    CONFIG_CLICK = auto()
    ERASE_CLICK = auto()
    MOVE_CLICK = auto()

class ReviewEventType(StrEnum):
    MENU_CLICK = auto()
    PREVIOUS_CLICK = auto()
    NEXT_CLICK = auto()

class BrowserEventType(StrEnum):
    MENU_CLICK = auto()
    BROWSER_STRIP_CLICK = auto()
    COPY_CLICK = auto()
    DELETE_CLICK = auto()
    REVIEW_CLICK = auto()
    FILTER_COLUMN_CLICK = auto()
    FILTER_ASCEND_CLICK = auto()
    PAGE_CLICK = auto()

class GameEventType(StrEnum):
    BOARD_CLICK = auto()
    PIECE_CLICK = auto()
    EMPTY_CLICK = auto()
    PAUSE_CLICK = auto()
    MENU_CLICK = auto()
    GAME_CLICK = auto()
    UPDATE_PIECES = auto()
    ROTATE_PIECE = auto()
    SET_LASER = auto()
    RESIGN_CLICK = auto()
    DRAW_CLICK = auto()
    TIMER_END = auto()

class MenuEventType(StrEnum):
    CONFIG_CLICK = auto()
    SETTINGS_CLICK = auto()
    BROWSER_CLICK = auto()

class SettingsEventType(StrEnum):
    RESET_DEFAULT = auto()
    RESET_USER = auto()
    MENU_CLICK = auto()
    COLOUR_SLIDER_SLIDE = auto()
    COLOUR_SLIDER_CLICK = auto()
    COLOUR_PICKER_HOVER = auto()
    PRIMARY_COLOUR_PICKER_CLICK = auto()
    SECONDARY_COLOUR_PICKER_CLICK = auto()
    PRIMARY_COLOUR_BUTTON_CLICK = auto()
    SECONDARY_COLOUR_BUTTON_CLICK = auto()
    VOLUME_SLIDER_SLIDE = auto()
    VOLUME_SLIDER_CLICK = auto()
    SHADER_PICKER_CLICK = auto()
    OPENGL_CLICK = auto()
    DROPDOWN_CLICK = auto()
    PARTICLES_CLICK = auto()

class ConfigEventType(StrEnum):
    GAME_CLICK = auto()
    MENU_CLICK = auto()
    FEN_STRING_TYPE = auto()
    TIME_TYPE = auto()
    TIME_CLICK = auto()
    PVP_CLICK = auto()
    PVC_CLICK = auto()
    CPU_DEPTH_CLICK = auto()
    PRESET_CLICK = auto()
    SETUP_CLICK = auto()
    COLOUR_CLICK = auto()

class Colour(IntEnum):
    BLUE = 0
    RED = 1

    def get_flipped_colour(self):
        if self == Colour.BLUE:
            return Colour.RED
        elif self == Colour.RED:
            return Colour.BLUE

class Piece(StrEnum):
    SPHINX = 's'
    PYRAMID = 'p'
    ANUBIS = 'n'
    SCARAB = 'r'
    PHAROAH = 'f'

class Score(IntEnum):
    PHAROAH = 0
    SPHINX = 0
    PYRAMID = 100
    ANUBIS = 110
    SCARAB = 200
    
    MOVE = 7
    POSITION = 11
    CHECKMATE = 100000
    INFINITE = 6969696969

class Rank(IntEnum):
    ONE = 0
    TWO = 1
    THREE = 2
    FOUR = 3
    FIVE = 4
    SIX = 5
    SEVEN = 6
    EIGHT = 7

class File(IntEnum):
    A = 0
    B = 1
    C = 2
    D = 3
    E = 4
    F = 5
    G = 6
    H = 7
    I = 8
    J = 9

class Rotation(StrEnum):
    UP = 'a'
    RIGHT = 'b'
    DOWN = 'c'
    LEFT = 'd'

    def to_angle(self):
        if self == Rotation.UP:
            return 0
        elif self == Rotation.RIGHT:
            return 270
        elif self == Rotation.DOWN:
            return 180
        elif self == Rotation.LEFT:
            return 90
    
    def get_clockwise(self):
        if self == Rotation.UP:
            return Rotation.RIGHT
        elif self == Rotation.RIGHT:
            return Rotation.DOWN
        elif self == Rotation.DOWN:
            return Rotation.LEFT
        elif self == Rotation.LEFT:
            return Rotation.UP

    def get_anticlockwise(self):
        if self == Rotation.UP:
            return Rotation.LEFT
        elif self == Rotation.RIGHT:
            return Rotation.UP
        elif self == Rotation.DOWN:
            return Rotation.RIGHT
        elif self == Rotation.LEFT:
            return Rotation.DOWN
    
    def get_opposite(self):
        return self.get_clockwise().get_clockwise()

class RotationIndex(IntEnum):
    FIRSTBIT = 0
    SECONDBIT = 1

class RotationDirection(StrEnum):
    CLOCKWISE = 'cw'
    ANTICLOCKWISE = 'acw'

    def get_opposite(self):
        if self == RotationDirection.CLOCKWISE:
            return RotationDirection.ANTICLOCKWISE
        elif self == RotationDirection.ANTICLOCKWISE:
            return RotationDirection.CLOCKWISE

class MoveType(StrEnum):
    MOVE = 'm'
    ROTATE = 'r'

class ImageType(StrEnum):
    HIGH_RES = 'high'
    LOW_RES = 'low'
    EMPTY = 'empty'

class LaserType(IntEnum):
    END = 0
    STRAIGHT = 1
    CORNER = 2

class LaserDirection(IntEnum):
    FROM_TOP = 1
    FROM_RIGHT = 2
    FROM_BOTTOM = 3
    FROM_LEFT = 4