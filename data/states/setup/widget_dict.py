from data.widgets import *
from data.components.custom_event import CustomEvent
from data.constants import SetupEventType, RotationDirection
from data.assets import GRAPHICS
from data.constants import Piece, Colour
from data.utils.asset_helpers import get_dimmed_icon

from data.managers.theme import theme

blue_pieces_container = Rectangle(
    relative_position=(-0.25, 0),
    relative_size=(0.05, 0.5),
    anchor_y='center',
    anchor_x='center'
)

red_pieces_container = Rectangle(
    relative_position=(0.25, 0),
    relative_size=(0.05, 0.5),
    anchor_y='center',
    anchor_x='center'
)

SETUP_WIDGETS = {
    'default': [
        red_pieces_container,
        blue_pieces_container,
        IconButton(
            relative_position=(0.1, 0.02),
            relative_size=(0.05, 0.1),
            icon=GRAPHICS['home'],
            border_width=5,
            border_radius=5,
            margin=10,
            anchor_x='right',
            fixed_position=True,
            event=CustomEvent(SetupEventType.MENU_CLICK)
        ),
        IconButton(
            relative_position=(-0.025, 0.15),
            relative_size=(0.1, 0.1),
            anchor_y='bottom',
            anchor_x='center',
            margin=10,
            icon=GRAPHICS['clockwise_arrow'],
            scale_mode='height',
            event=CustomEvent(SetupEventType.ROTATE_PIECE_CLICK, rotation_direction=RotationDirection.CLOCKWISE)
        ),
        IconButton(
            relative_position=(0.025, 0.15),
            relative_size=(0.1, 0.1),
            anchor_y='bottom',
            anchor_x='center',
            margin=10,
            icon=GRAPHICS['anticlockwise_arrow'],
            scale_mode='height',
            event=CustomEvent(SetupEventType.ROTATE_PIECE_CLICK, rotation_direction=RotationDirection.ANTICLOCKWISE)
        ),
        IconButton(
            relative_position=(0.1, 0.8),
            relative_size=(0.1, 0.1),
            scale_mode='height',
            margin=10,
            border_width=5,
            border_radius=10,
            icon=GRAPHICS['copy'],
            event=CustomEvent(SetupEventType.COPY_CLICK),
        ),
        IconButton(
            relative_position=(0.25, 0.8),
            relative_size=(0.1, 0.1),
            scale_mode='height',
            margin=10,
            border_width=5,
            border_radius=10,
            fill_colour=(255, 0, 0),
            icon=GRAPHICS['trash'],
            event=CustomEvent(SetupEventType.EMPTY_CLICK),
        ),
        IconButton(
            relative_position=(0.3, 0.8),
            relative_size=(0.1, 0.1),
            scale_mode='height',
            margin=10,
            border_width=5,
            border_radius=10,
            fill_colour=(255, 0, 0),
            icon=GRAPHICS['reset'],
            event=CustomEvent(SetupEventType.RESET_CLICK),
        ),
        IconButton(
            relative_position=(0.2, 0.8),
            relative_size=(0.1, 0.1),
            scale_mode='height',
            margin=10,
            border_width=5,
            border_radius=10,
            fill_colour=(0, 255, 0),
            icon=GRAPHICS['right_arrow'],
            event=CustomEvent(SetupEventType.START_CLICK),
        ),
        IconButton(
            relative_position=(0.1, 0.1),
            relative_size=(0.1, 0.1),
            scale_mode='height',
            margin=10,
            border_width=5,
            border_radius=10,
            icon=GRAPHICS['return'],
            event=CustomEvent(SetupEventType.CONFIG_CLICK),
        )
    ],
    'blue_piece_buttons': {},
    'red_piece_buttons': {},
    'erase_button':
    MultipleIconButton(
        relative_position=(0.2, 0.1),
        relative_size=(0.1, 0.1),
        scale_mode='height',
        margin=10,
        border_width=5,
        border_radius=10,
        icons_dict={True: GRAPHICS['erase'], False: get_dimmed_icon(GRAPHICS['erase'])},
        event=CustomEvent(SetupEventType.ERASE_CLICK),
    ),
    'move_button':
    MultipleIconButton(
        relative_position=(0.3, 0.1),
        relative_size=(0.1, 0.1),
        scale_mode='height',
        margin=10,
        border_width=5,
        border_radius=10,
        icons_dict={True: GRAPHICS['point'], False: get_dimmed_icon(GRAPHICS['point'])},
        event=CustomEvent(SetupEventType.MOVE_CLICK),
    ),
    'chessboard':
    Chessboard(
        relative_position=(0, 0),
        relative_width=0.4,
        scale_mode='width',
        anchor_x='center',
        anchor_y='center'
    ),
    'blue_start_button':
    MultipleIconButton(
        relative_position=(0.05, 0.55),
        relative_size=(0.1, 0.1),
        scale_mode='height',
        margin=0,
        border_width=5,
        border_radius=5,
        icons_dict={False: get_dimmed_icon(GRAPHICS['pharoah_1']), True: GRAPHICS['pharoah_1']},
        event=CustomEvent(SetupEventType.BLUE_START_CLICK)
    ),
    'red_start_button':
    MultipleIconButton(
        relative_position=(0.15, 0.55),
        relative_size=(0.1, 0.1),
        scale_mode='height',
        margin=0,
        border_width=5,
        border_radius=5,
        icons_dict={True: GRAPHICS['pharoah_2'], False: get_dimmed_icon(GRAPHICS['pharoah_2'])},
        event=CustomEvent(SetupEventType.RED_START_CLICK)
    )
}

for index, piece in enumerate([piece for piece in Piece if piece != Piece.SPHINX]):
    blue_icon = GRAPHICS[f'{piece.name.lower()}_1']
    dimmed_blue_icon = get_dimmed_icon(blue_icon)

    SETUP_WIDGETS['blue_piece_buttons'][piece] = MultipleIconButton(
        parent=blue_pieces_container,
        relative_position=(0, index / 4),
        relative_size=(0.25, 0.25),
        scale_mode='height',
        anchor_x='center',
        margin=10,
        icons_dict={True: blue_icon, False: dimmed_blue_icon},
        event=CustomEvent(SetupEventType.PICK_PIECE_CLICK, piece=piece, active_colour=Colour.BLUE)
    )

    red_icon = GRAPHICS[f'{piece.name.lower()}_2']
    dimmed_red_icon = get_dimmed_icon(red_icon)

    SETUP_WIDGETS['red_piece_buttons'][piece] = MultipleIconButton(
        parent=red_pieces_container,
        relative_position=(0, index / 4),
        relative_size=(0.25, 0.25),
        scale_mode='height',
        anchor_x='center',
        margin=10,
        icons_dict={True: red_icon, False: dimmed_red_icon},
        event=CustomEvent(SetupEventType.PICK_PIECE_CLICK, piece=piece, active_colour=Colour.RED)
    )