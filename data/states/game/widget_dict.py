from data.components.widgets import *
from data.components.custom_event import CustomEvent
from data.constants import GameEventType, RotationDirection

GAME_WIDGETS = {
    'default': [
        TextButton(
            relative_position=(0.1, 0.2),
            text='CLOCKWISE',
            text_colour=(255, 0, 0),
            font_size=50,
            event=CustomEvent(GameEventType.ROTATE_PIECE, rotation_direction=RotationDirection.CLOCKWISE)
        ),
        TextButton(
            relative_position=(0.1, 0.4),
            text='ANTICLOCKWISE',
            text_colour=(0, 255, 0),
            font_size=50,
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