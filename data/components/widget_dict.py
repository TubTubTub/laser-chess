from data.components.widgets import *
from data.components.custom_event import CustomEvent
from data.constants import GameEventType, MenuEventType, SettingsEventType, ConfigEventType, RotationDirection
from data.setup import GRAPHICS

WIDGET_DICT = {
    'game': [
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
    ],
    'pause': [
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
    ],
    'win': [
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
    ],
    'menu': [
        TextButton(
            relative_position=(0.5, 0.5),
            text='START GAME',
            text_colour=(255, 0, 0),
            font_size=50,
            fill_colour=(255, 255, 0),
            border_width=5,
            event=CustomEvent(MenuEventType.CONFIG_CLICK)
        ),
        TextButton(
            relative_position=(0.5, 0.8),
            text='SETTINGS',
            text_colour=(255, 0, 0),
            font_size=50,
            fill_colour=(0, 0, 255),
            event=CustomEvent(MenuEventType.SETTINGS_CLICK)
        ),
        IconButton(
            relative_position=(0.1, 0.1),
            size=(150, 150),
            icon=GRAPHICS['home'],
            event=CustomEvent(MenuEventType.SETTINGS_CLICK)
        ),
        Icon(
            relative_position=(0.2, 0.1),
            size=(150, 150),
            icon=GRAPHICS['home'],
        )
    ],
    'settings': [
        TextButton(
            relative_position=(0.5, 0.2),
            text='RETURN TO MAIN MENU',
            text_colour=(255, 0, 0),
            font_size=50,
            event=CustomEvent(SettingsEventType.MENU_CLICK)
        ),
        TextButton(
            relative_position=(0.5, 0.4),
            text='UPDATE PRIMARY COLOUR',
            text_colour=(255, 0, 0),
            font_size=50,
            event=CustomEvent(SettingsEventType.UPDATE_PRIMARY)
        ),
        TextButton(
            relative_position=(0.5, 0.6),
            text='RESET TO DEFAULT',
            text_colour=(255, 0, 0),
            font_size=50,
            event=CustomEvent(SettingsEventType.RESET_DEFAULT)
        ),
        Switch(
            relative_position=(0.2, 0.8),
            relative_length=(0.1),
            colour=(0, 0, 255),
            event=CustomEvent(SettingsEventType.RESET_DEFAULT)
        )
    ],
    'config': [
        TextButton(
            relative_position=(0.5, 0.2),
            text='START NEW GAME',
            text_colour=(255, 0, 0),
            font_size=50,
            event=CustomEvent(ConfigEventType.GAME_CLICK)
        ),
        TextButton(
            relative_position=(0.5, 0.5),
            text='RETURN TO MAIN MENU',
            text_colour=(255, 0, 0),
            font_size=50,
            event=CustomEvent(ConfigEventType.MENU_CLICK)
        ),
    ]
}