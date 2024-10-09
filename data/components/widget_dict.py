from data.components.widgets import Text, Button
from data.components.custom_event import CustomEvent
from data.constants import GameEventType, MenuEventType, SettingsEventType, ConfigEventType, RotationDirection

WIDGET_DICT = {
    'game': [
        Text(
            relative_position=(0, 200),
            text='CLOCKWISE',
            text_colour=(255, 0, 0),
            font_size=50
        ),
        Text(
            relative_position=(0, 400),
            text='ANTICLOCKWISE',
            text_colour=(0, 255, 0),
            font_size=50
        )
    ],
    'pause': [
        Text(
            relative_position=(400, 200),
            text='GO TO MENU',
            text_colour=(255, 0, 0),
            font_size=50
        ),
        Text(
            relative_position=(400, 400),
            text='RESUME GAME',
            text_colour=(255, 0, 0),
            font_size=50
        )
    ],
    'win': [
        Text(
            relative_position=(400, 200),
            text='GO TO MENU',
            text_colour=(255, 0, 0),
            font_size=50
        ),
        Text(
            relative_position=(400, 400),
            text='NEW GAME',
            text_colour=(255, 0, 0),
            font_size=50
        )
    ],
    'menu': [
        Button(
            relative_position=(0.5, 0.5),
            text='START GAME',
            text_colour=(255, 0, 0),
            font_size=50,
            fill_colour=(255, 255, 0),
            event=MenuEventType.CONFIG_CLICK
        ),
        Button(
            relative_position=(0.5, 0.8),
            text='SETTINGS',
            text_colour=(255, 0, 0),
            font_size=50,
            fill_colour=(0, 0, 255),
            event=MenuEventType.SETTINGS_CLICK
        ),
    ],
    'settings': [
        Text(
            relative_position=(400, 200),
            text='RETURN TO MAIN MENU',
            text_colour=(255, 0, 0),
            font_size=50
        ),
        Text(
            relative_position=(400, 500),
            text='UPDATE PRIMARY COLOUR',
            text_colour=(255, 0, 0),
            font_size=50
        ),
        Text(
            relative_position=(300, 100),
            text='RESET TO DEFAULT',
            text_colour=(255, 0, 0),
            font_size=50
        ),
    ],
    'config': [
        Text(
            relative_position=(400, 200),
            text='START NEW GAME',
            text_colour=(255, 0, 0),
            font_size=50
        ),
        Text(
            relative_position=(400, 300),
            text='RETURN TO MAIN MENU',
            text_colour=(255, 0, 0),
            font_size=50
        ),
    ]
}