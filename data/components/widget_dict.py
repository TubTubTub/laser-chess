from data.components.widgets import *
from data.components.custom_event import CustomEvent
from data.constants import GameEventType, MenuEventType, SettingsEventType, ConfigEventType, RotationDirection

WIDGET_DICT = {
    'game': [
        Button(
            relative_position=(0.1, 0.2),
            text='CLOCKWISE',
            text_colour=(255, 0, 0),
            font_size=50,
            event=CustomEvent(GameEventType.ROTATE_PIECE, rotation_direction=RotationDirection.CLOCKWISE)
        ),
        Button(
            relative_position=(0.1, 0.4),
            text='ANTICLOCKWISE',
            text_colour=(0, 255, 0),
            font_size=50,
            event=CustomEvent(GameEventType.ROTATE_PIECE, rotation_direction=RotationDirection.ANTICLOCKWISE)
        )
    ],
    'pause': [
        Button(
            relative_position=(0.5, 0.2),
            text='GO TO MENU',
            text_colour=(255, 0, 0),
            font_size=50,
            event=CustomEvent(GameEventType.MENU_CLICK)
        ),
        Button(
            relative_position=(0.5, 0.4),
            text='RESUME GAME',
            text_colour=(255, 0, 0),
            font_size=50,
            event=CustomEvent(GameEventType.PAUSE_CLICK)
        )
    ],
    'win': [
        Button(
            relative_position=(0.5, 0.2),
            text='GO TO MENU',
            text_colour=(255, 0, 0),
            font_size=50,
            event=CustomEvent(GameEventType.MENU_CLICK)
        ),
        Button(
            relative_position=(0.5, 0.4),
            text='NEW GAME',
            text_colour=(255, 0, 0),
            font_size=50,
            event=CustomEvent(GameEventType.GAME_CLICK)
        )
    ],
    'menu': [
        Button(
            relative_position=(0.5, 0.5),
            text='START GAME',
            text_colour=(255, 0, 0),
            font_size=50,
            fill_colour=(255, 255, 0),
            event=CustomEvent(MenuEventType.CONFIG_CLICK)
        ),
        Button(
            relative_position=(0.5, 0.8),
            text='SETTINGS',
            text_colour=(255, 0, 0),
            font_size=50,
            fill_colour=(0, 0, 255),
            event=CustomEvent(MenuEventType.SETTINGS_CLICK)
        ),
        # ColourPicker(
        #     origin_position=(0.5, 0.5)
        # ),
        ColourSlider(
            relative_position=(0, 0.1),
            width=1000,
            height=200,
        )
    ],
    'settings': [
        Button(
            relative_position=(0.5, 0.2),
            text='RETURN TO MAIN MENU',
            text_colour=(255, 0, 0),
            font_size=50,
            event=CustomEvent(SettingsEventType.MENU_CLICK)
        ),
        Button(
            relative_position=(0.5, 0.4),
            text='UPDATE PRIMARY COLOUR',
            text_colour=(255, 0, 0),
            font_size=50,
            event=CustomEvent(SettingsEventType.UPDATE_PRIMARY)
        ),
        Button(
            relative_position=(0.5, 0.6),
            text='RESET TO DEFAULT',
            text_colour=(255, 0, 0),
            font_size=50,
            event=CustomEvent(SettingsEventType.RESET_DEFAULT)
        ),
    ],
    'config': [
        Button(
            relative_position=(0.5, 0.2),
            text='START NEW GAME',
            text_colour=(255, 0, 0),
            font_size=50,
            event=CustomEvent(ConfigEventType.GAME_CLICK)
        ),
        Button(
            relative_position=(0.5, 0.5),
            text='RETURN TO MAIN MENU',
            text_colour=(255, 0, 0),
            font_size=50,
            event=CustomEvent(ConfigEventType.MENU_CLICK)
        ),
    ]
}