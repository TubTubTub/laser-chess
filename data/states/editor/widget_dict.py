from data.widgets import *
from data.components.custom_event import CustomEvent
from data.constants import SetupEventType, RotationDirection
from data.assets import GRAPHICS
from data.constants import Piece, Colour
from data.utils.asset_helpers import get_dimmed_icon

from data.managers.theme import theme

blue_pieces_container = Rectangle(
    relative_position=(0.25, 0),
    relative_size=(0.13, 0.65),
    scale_mode='height',
    anchor_y='center',
    anchor_x='center'
)

red_pieces_container = Rectangle(
    relative_position=(-0.25, 0),
    relative_size=(0.13, 0.65),
    scale_mode='height',
    anchor_y='center',
    anchor_x='center'
)

bottom_actions_container = Rectangle(
    relative_position=(0, 0.05),
    relative_size=(0.4, 0.1),
    anchor_x='center',
    anchor_y='bottom'
)

top_actions_container = Rectangle(
    relative_position=(0, 0.05),
    relative_size=(0.3, 0.1),
    anchor_x='center',
    scale_mode='height'
)

EDITOR_WIDGETS = {
    'default': [
        red_pieces_container,
        blue_pieces_container,
        bottom_actions_container,
        top_actions_container,
        ReactiveIconButton(
            relative_position=(0, 0),
            relative_size=(0.075, 0.075),
            anchor_x='right',
            scale_mode='height',
            base_icon=GRAPHICS['home_base'],
            hover_icon=GRAPHICS['home_hover'],
            press_icon=GRAPHICS['home_press'],
            fixed_position=(5, 5),
            event=CustomEvent(SetupEventType.MENU_CLICK)
        ),
        ReactiveIconButton(
            parent=bottom_actions_container,
            relative_position=(0.06, 0),
            relative_size=(1, 1),
            anchor_x='center',
            scale_mode='height',
            base_icon=GRAPHICS['clockwise_arrow_base'],
            hover_icon=GRAPHICS['clockwise_arrow_hover'],
            press_icon=GRAPHICS['clockwise_arrow_press'],
            event=CustomEvent(SetupEventType.ROTATE_PIECE_CLICK, rotation_direction=RotationDirection.CLOCKWISE)
        ),
        ReactiveIconButton(
            parent=bottom_actions_container,
            relative_position=(-0.06, 0),
            relative_size=(1, 1),
            anchor_x='center',
            scale_mode='height',
            base_icon=GRAPHICS['anticlockwise_arrow_base'],
            hover_icon=GRAPHICS['anticlockwise_arrow_hover'],
            press_icon=GRAPHICS['anticlockwise_arrow_press'],
            event=CustomEvent(SetupEventType.ROTATE_PIECE_CLICK, rotation_direction=RotationDirection.ANTICLOCKWISE)
        ),
        ReactiveIconButton(
            parent=top_actions_container,
            relative_position=(0, 0),
            relative_size=(1, 1),
            scale_mode='height',
            anchor_x='right',
            base_icon=GRAPHICS['copy_base'],
            hover_icon=GRAPHICS['copy_hover'],
            press_icon=GRAPHICS['copy_press'],
            event=CustomEvent(SetupEventType.COPY_CLICK),
        ),
        ReactiveIconButton(
            parent=top_actions_container,
            relative_position=(0, 0),
            relative_size=(1, 1),
            scale_mode='height',
            base_icon=GRAPHICS['delete_base'],
            hover_icon=GRAPHICS['delete_hover'],
            press_icon=GRAPHICS['delete_press'],
            event=CustomEvent(SetupEventType.EMPTY_CLICK),
        ),
        ReactiveIconButton(
            parent=top_actions_container,
            relative_position=(0, 0),
            relative_size=(1, 1),
            scale_mode='height',
            anchor_x='center',
            base_icon=GRAPHICS['discard_arrow_base'],
            hover_icon=GRAPHICS['discard_arrow_hover'],
            press_icon=GRAPHICS['discard_arrow_press'],
            event=CustomEvent(SetupEventType.RESET_CLICK),
        ),
        ReactiveIconButton(
            relative_position=(0, 0),
            fixed_position=(10, 0),
            relative_size=(0.1, 0.1),
            anchor_x='right',
            anchor_y='center',
            scale_mode='height',
            base_icon=GRAPHICS['play_arrow_base'],
            hover_icon=GRAPHICS['play_arrow_hover'],
            press_icon=GRAPHICS['play_arrow_press'],
            event=CustomEvent(SetupEventType.START_CLICK),
        ),
        ReactiveIconButton(
            relative_position=(0, 0),
            fixed_position=(10, 0),
            relative_size=(0.1, 0.1),
            anchor_y='center',
            scale_mode='height',
            base_icon=GRAPHICS['return_arrow_base'],
            hover_icon=GRAPHICS['return_arrow_hover'],
            press_icon=GRAPHICS['return_arrow_press'],
            event=CustomEvent(SetupEventType.CONFIG_CLICK),
        )
    ],
    'blue_piece_buttons': {},
    'red_piece_buttons': {},
    'erase_button':
    MultipleIconButton(
        parent=red_pieces_container,
        relative_position=(0, 0),
        relative_size=(0.2, 0.2),
        scale_mode='height',
        margin=10,
        border_width=5,
        border_radius=10,
        icons_dict={True: GRAPHICS['erase'], False: get_dimmed_icon(GRAPHICS['erase'])},
        event=CustomEvent(SetupEventType.ERASE_CLICK),
    ),
    'move_button':
    MultipleIconButton(
        parent=blue_pieces_container,
        relative_position=(0, 0),
        relative_size=(0.2, 0.2),
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
        parent=bottom_actions_container,
        relative_position=(0, 0),
        relative_size=(1, 1),
        scale_mode='height',
        anchor_x='right',
        margin=0,
        border_width=5,
        border_radius=5,
        icons_dict={False: get_dimmed_icon(GRAPHICS['pharoah_1']), True: GRAPHICS['pharoah_1']},
        event=CustomEvent(SetupEventType.BLUE_START_CLICK)
    ),
    'red_start_button':
    MultipleIconButton(
        parent=bottom_actions_container,
        relative_position=(0, 0),
        relative_size=(1, 1),
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

    EDITOR_WIDGETS['blue_piece_buttons'][piece] = MultipleIconButton(
        parent=blue_pieces_container,
        relative_position=(0, (index + 1) / 5),
        relative_size=(0.2, 0.2),
        scale_mode='height',
        margin=10,
        icons_dict={True: blue_icon, False: dimmed_blue_icon},
        event=CustomEvent(SetupEventType.PICK_PIECE_CLICK, piece=piece, active_colour=Colour.BLUE)
    )

    red_icon = GRAPHICS[f'{piece.name.lower()}_2']
    dimmed_red_icon = get_dimmed_icon(red_icon)

    EDITOR_WIDGETS['red_piece_buttons'][piece] = MultipleIconButton(
        parent=red_pieces_container,
        relative_position=(0, (index + 1) / 5),
        relative_size=(0.2, 0.2),
        scale_mode='height',
        margin=10,
        icons_dict={True: red_icon, False: dimmed_red_icon},
        event=CustomEvent(SetupEventType.PICK_PIECE_CLICK, piece=piece, active_colour=Colour.RED)
    )