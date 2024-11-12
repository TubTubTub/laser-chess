from data.widgets import *
from data.components.custom_event import CustomEvent
from data.constants import GameEventType, RotationDirection, Colour
from data.assets import GRAPHICS

GAME_WIDGETS_PVC = {
    'default': [
        IconButton(
            relative_position=(0.52, 0.85),
            size=(60, 60),
            margin=10,
            icon=GRAPHICS['clockwise_arrow'],
            event=CustomEvent(GameEventType.ROTATE_PIECE, rotation_direction=RotationDirection.CLOCKWISE)
        ),
        IconButton(
            relative_position=(0.44, 0.85),
            size=(60, 60),
            margin=10,
            icon=GRAPHICS['anticlockwise_arrow'],
            event=CustomEvent(GameEventType.ROTATE_PIECE, rotation_direction=RotationDirection.ANTICLOCKWISE)
        ),
        TextButton(
            relative_position=(0.27, 0.85),
            text="   Resign",
            font_size=30,
            margin=25,
            event=CustomEvent(GameEventType.RESIGN_CLICK)
        ),
        TextButton(
            relative_position=(0.65, 0.85),
            text="   Draw",
            font_size=30,
            margin=25,
            event=CustomEvent(GameEventType.DRAW_CLICK)
        ),
        Icon(
            relative_position=(0.27, 0.85),
            size=(30, 30),
            fill_colour=(0, 0, 0, 0),
            border_radius=0,
            margin=0,
            icon=GRAPHICS['resign']
        ),
        Icon(
            relative_position=(0.65, 0.85),
            size=(35, 35),
            fill_colour=(0, 0, 0, 0),
            border_radius=0,
            margin=0,
            icon=GRAPHICS['draw']
        )
    ],
    'blue_timer':
    Timer(
        relative_position=(0.02, 0.18),
        active_colour=Colour.BLUE,
        event_type=GameEventType.TIMER_END,
    ),
    'red_timer':
    Timer(
        relative_position=(0.1, 0.3),
        active_colour=Colour.RED,
        event_type=GameEventType.TIMER_END,
    ),
    'status_text':
    Text(
        relative_position=(0.3, 0.06),
        font_size=40,
        margin=10,
        text="",
        minimum_width=400
    )
}

GAME_WIDGETS_PVP = {
    'default': [
        IconButton(
            relative_position=(0.52, 0.85),
            size=(60, 60),
            margin=10,
            icon=GRAPHICS['clockwise_arrow'],
            event=CustomEvent(GameEventType.ROTATE_PIECE, rotation_direction=RotationDirection.CLOCKWISE)
        ),
        IconButton(
            relative_position=(0.44, 0.85),
            size=(60, 60),
            margin=10,
            icon=GRAPHICS['anticlockwise_arrow'],
            event=CustomEvent(GameEventType.ROTATE_PIECE, rotation_direction=RotationDirection.ANTICLOCKWISE)
        ),
        TextButton(
            relative_position=(0.27, 0.85),
            text="   Resign",
            font_size=30,
            margin=25,
            event=CustomEvent(GameEventType.RESIGN_CLICK)
        ),
        TextButton(
            relative_position=(0.65, 0.85),
            text="   Draw",
            font_size=30,
            margin=25,
            event=CustomEvent(GameEventType.DRAW_CLICK)
        ),
        Icon(
            relative_position=(0.27, 0.85),
            size=(30, 30),
            fill_colour=(0, 0, 0, 0),
            border_radius=0,
            margin=0,
            icon=GRAPHICS['resign']
        ),
        Icon(
            relative_position=(0.65, 0.85),
            size=(35, 35),
            fill_colour=(0, 0, 0, 0),
            border_radius=0,
            margin=0,
            icon=GRAPHICS['draw']
        )
    ],
    'blue_timer':
    Timer(
        relative_position=(0.02, 0.18),
        active_colour=Colour.BLUE,
        event_type=GameEventType.TIMER_END,
    ),
    'red_timer':
    Timer(
        relative_position=(0.02, 0.62),
        active_colour=Colour.RED,
        event_type=GameEventType.TIMER_END,
    ),
    'status_text':
    Text(
        relative_position=(0.3, 0.06),
        font_size=40,
        margin=10,
        text="",
        minimum_width=400
    )
}

PAUSE_WIDGETS = {
    'default': [
        TextButton(
            relative_position=(0.36, 0.3),
            text='GO TO MENU',
            text_colour=(255, 0, 0),
            font_size=50,
            event=CustomEvent(GameEventType.MENU_CLICK)
        ),
        TextButton(
            relative_position=(0.35, 0.5),
            text='RESUME GAME',
            text_colour=(255, 0, 0),
            font_size=50,
            event=CustomEvent(GameEventType.PAUSE_CLICK)
        )
    ]
}

WIN_WIDGETS = {
    'default': [
        Rectangle(
            relative_position=(0.3, 0.25),
            size=(450, 210),
            fill_colour=(128, 128, 128, 200),
        ),
        TextButton(
            relative_position=(0.5, 0.27),
            text='GO TO MENU',
            text_colour=(255, 0, 0),
            font_size=50,
            event=CustomEvent(GameEventType.MENU_CLICK)
        ),
        TextButton(
            relative_position=(0.5, 0.43),
            text='NEW GAME',
            text_colour=(255, 0, 0),
            font_size=50,
            event=CustomEvent(GameEventType.GAME_CLICK)
        ),
    ],
    'blue_trophy':
    Icon(
        relative_position=(0.3, 0.26),
        size=(200, 200),
        margin=0,
        icon=GRAPHICS['blue_trophy'],
        fill_colour=(0, 0, 0, 0),
    ),
    'red_trophy':
    Icon(
        relative_position=(0.3, 0.26),
        size=(200, 200),
        margin=0,
        icon=GRAPHICS['red_trophy'],
        fill_colour=(0, 0, 0, 0),
    ),
    'draw_trophy':
    Icon(
        relative_position=(0.3, 0.26),
        size=(200, 200),
        margin=0,
        icon=GRAPHICS['hug'],
        fill_colour=(0, 0, 0, 0),
    )
}