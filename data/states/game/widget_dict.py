from data.widgets import *
from data.components.custom_event import CustomEvent
from data.constants import GameEventType, RotationDirection
from data.assets import GRAPHICS

GAME_WIDGETS_PVC = {
    'default': [
        IconButton(
            relative_position=(0.44, 0.85),
            size=(60, 60),
            margin=10,
            icon=GRAPHICS['clockwise_arrow'],
            event=CustomEvent(GameEventType.ROTATE_PIECE, rotation_direction=RotationDirection.CLOCKWISE)
        ),
        IconButton(
            relative_position=(0.52, 0.85),
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
    ]
}

GAME_WIDGETS_PVP = {
    'default': [
        IconButton(
            relative_position=(0.44, 0.85),
            size=(60, 60),
            margin=10,
            icon=GRAPHICS['clockwise_arrow'],
            event=CustomEvent(GameEventType.ROTATE_PIECE, rotation_direction=RotationDirection.CLOCKWISE)
        ),
        IconButton(
            relative_position=(0.52, 0.85),
            size=(60, 60),
            margin=10,
            icon=GRAPHICS['anticlockwise_arrow'],
            event=CustomEvent(GameEventType.ROTATE_PIECE, rotation_direction=RotationDirection.ANTICLOCKWISE)
        )
    ]
}

PAUSE_WIDGETS = {
    'default': [
        TextButton(
            relative_position=(0.5, 0.2),
            text='GO TO MENU',
            text_colour=(255, 0, 0),
            font_size=50,
            event=CustomEvent(GameEventType.MENU_CLICK)
        ),
        TextButton(
            relative_position=(0.5, 0.4),
            text='RESUME GAME',
            text_colour=(255, 0, 0),
            font_size=50,
            event=CustomEvent(GameEventType.PAUSE_CLICK)
        )
    ]
}

WIN_WIDGETS = {
    'default': [
        TextButton(
            relative_position=(0.5, 0.2),
            text='GO TO MENU',
            text_colour=(255, 0, 0),
            font_size=50,
            event=CustomEvent(GameEventType.MENU_CLICK)
        ),
        TextButton(
            relative_position=(0.5, 0.4),
            text='NEW GAME',
            text_colour=(255, 0, 0),
            font_size=50,
            event=CustomEvent(GameEventType.GAME_CLICK)
        )
    ]
}