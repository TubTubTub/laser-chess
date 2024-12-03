from data.widgets import *
from data.components.custom_event import CustomEvent
from data.constants import GameEventType, RotationDirection, Colour
from data.assets import GRAPHICS

move_list = MoveList(
    relative_position=(0, 0),
    relative_width=0.2,
    minimum_height=390,
    move_list=[]
)

GAME_WIDGETS = {
    'default': [
        IconButton(
            relative_position=(0.52, 0.85),
            relative_size=(0.3, 0.3),
            margin=10,
            icon=GRAPHICS['clockwise_arrow'],
            event=CustomEvent(GameEventType.ROTATE_PIECE, rotation_direction=RotationDirection.CLOCKWISE)
        ),
        IconButton(
            relative_position=(0.44, 0.85),
            relative_size=(0.3, 0.3),
            margin=10,
            icon=GRAPHICS['anticlockwise_arrow'],
            event=CustomEvent(GameEventType.ROTATE_PIECE, rotation_direction=RotationDirection.ANTICLOCKWISE)
        ),
        TextButton(
            relative_position=(0.27, 0.85),
            relative_size=(0.1, 0.1),
            text="   Resign",
            margin=1,
            event=CustomEvent(GameEventType.RESIGN_CLICK)
        ),
        TextButton(
            relative_position=(0.65, 0.85),
            relative_size=(0.1, 0.1),
            text="   Draw",
            margin=1,
            event=CustomEvent(GameEventType.DRAW_CLICK)
        ),
        Icon(
            relative_position=(0.27, 0.85),
            relative_size=(0.3, 0.3),
            fill_colour=(0, 0, 0, 0),
            border_radius=0,
            margin=0,
            icon=GRAPHICS['resign']
        ),
        Icon(
            relative_position=(0.65, 0.85),
            relative_size=(0.3, 0.3),
            fill_colour=(0, 0, 0, 0),
            border_radius=0,
            margin=0,
            icon=GRAPHICS['draw']
        )
    ],
    'blue_timer':
    Timer(
        relative_position=(0.02, 0.62),
        relative_size=(0.2, 0.2),
        active_colour=Colour.BLUE,
        event_type=GameEventType.TIMER_END,
    ),
    'red_timer':
    Timer(
        relative_position=(0.02, 0.18),
        relative_size=(0.2, 0.2),
        active_colour=Colour.RED,
        event_type=GameEventType.TIMER_END,
    ),
    'status_text':
    Text(
        relative_position=(0.3, 0.06),
        relative_size=(0.7, 0.2),
        margin=10,
        text="g",
        minimum_width=400
    ),
    'chessboard':
    Chessboard(
        relative_position=(0, 0),
        relative_width=0.5,
        center=True
    ),
    'move_list':
        move_list,
    'scroll_area':
    ScrollArea(
        relative_position=(0.77, 0.18),
        relative_size=(0.2, 0.4),
        vertical=True,
        widget=move_list
    )
}

PAUSE_WIDGETS = {
    'default': [
        TextButton(
            relative_position=(0.36, 0.3),
            relative_size=(0.3, 0.2),
            text='GO TO MENU',
            text_colour=(255, 0, 0),
            event=CustomEvent(GameEventType.MENU_CLICK)
        ),
        TextButton(
            relative_position=(0.35, 0.5),
            relative_size=(0.3, 0.2),
            text='RESUME GAME',
            text_colour=(255, 0, 0),
            event=CustomEvent(GameEventType.PAUSE_CLICK)
        )
    ]
}

WIN_WIDGETS = {
    'default': [
        Rectangle(
            relative_position=(0.3, 0.25),
            relative_size=(0.5, 0.3),
            fill_colour=(128, 128, 128, 200),
        ),
        TextButton(
            relative_position=(0.5, 0.27),
            relative_size=(0.3, 0.2),
            text='GO TO MENU',
            text_colour=(255, 0, 0),
            event=CustomEvent(GameEventType.MENU_CLICK)
        ),
        TextButton(
            relative_position=(0.5, 0.43),
            relative_size=(0.3, 0.2),
            text='NEW GAME',
            text_colour=(255, 0, 0),
            event=CustomEvent(GameEventType.GAME_CLICK)
        ),
    ],
    'blue_trophy':
    Icon(
        relative_position=(0.3, 0.26),
        relative_size=(0.3, 0.3),
        margin=0,
        icon=GRAPHICS['blue_trophy'],
        fill_colour=(0, 0, 0, 0),
    ),
    'red_trophy':
    Icon(
        relative_position=(0.3, 0.26),
        relative_size=(0.3, 0.3),
        margin=0,
        icon=GRAPHICS['red_trophy'],
        fill_colour=(0, 0, 0, 0),
    ),
    'draw_trophy':
    Icon(
        relative_position=(0.3, 0.26),
        relative_size=(0.3, 0.3),
        margin=0,
        icon=GRAPHICS['hug'],
        fill_colour=(0, 0, 0, 0),
    )
}