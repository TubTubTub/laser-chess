from data.widgets import *
from data.components.custom_event import CustomEvent
from data.constants import SetupEventType
from data.assets import GRAPHICS
from data.constants import Piece, Colour

from data.theme import theme

red_pieces_container = Rectangle(
    relative_position=(-0.25, 0),
    relative_size=(0.05, 0.5),
    anchor_y='center',
    anchor_x='center'
)

blue_pieces_container = Rectangle(
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
    ],
    'chessboard':
    Chessboard(
        relative_position=(0, 0),
        relative_width=0.4,
        scale_mode='width',
        anchor_x='center',
        anchor_y='center'
    ),
}

for index, piece_name in enumerate(['pyramid', 'scarab', 'anubis', 'pharoah']):
    SETUP_WIDGETS['default'].append(
        IconButton(
            parent=blue_pieces_container,
            relative_position=(0, index / 4),
            relative_size=(0.25, 0.25),
            scale_mode='height',
            anchor_x='center',
            margin=10,
            icon=GRAPHICS[f'{piece_name}_1'],
            event=CustomEvent(SetupEventType.PICK_PIECE_CLICK, piece=Piece[piece_name.upper()], colour=Colour.BLUE)
        )
    )

    SETUP_WIDGETS['default'].append(
        IconButton(
            parent=red_pieces_container,
            relative_position=(0, index / 4),
            relative_size=(0.25, 0.25),
            scale_mode='height',
            anchor_x='center',
            margin=10,
            icon=GRAPHICS[f'{piece_name}_2'],
            event=CustomEvent(SetupEventType.PICK_PIECE_CLICK, piece=Piece[piece_name.upper()], colour=Colour.RED)
        )
    )