from data.components.widgets import Text
from data.components.custom_event import CustomEvent
from data.constants import GameEventType, MenuEventType, SettingsEventType, ConfigEventType, RotationDirection

WIDGET_DICT = {
    'game': [
        Text(
            event=CustomEvent.create_event(GameEventType.ROTATE_PIECE, rotation_direction=RotationDirection.CLOCKWISE),
            position=(0, 200),
            text='CLOCKWISE',
            text_colour=(255, 0, 0),
            font_size=50
        ),
        Text(
            event=CustomEvent.create_event(GameEventType.ROTATE_PIECE, rotation_direction=RotationDirection.ANTICLOCKWISE),
            position=(0, 400),
            text='ANTICLOCKWISE',
            text_colour=(0, 255, 0),
            font_size=50
        )
    ],
    'pause': [
        Text(
            event=CustomEvent.create_event(GameEventType.MENU_CLICK),
            position=(400, 200),
            text='GO TO MENU',
            text_colour=(255, 0, 0),
            font_size=50
        ),
        Text(
            event=CustomEvent.create_event(GameEventType.PAUSE_CLICK),
            position=(400, 400),
            text='RESUME GAME',
            text_colour=(255, 0, 0),
            font_size=50
        )
    ],
    'win': [
        Text(
            event=CustomEvent.create_event(GameEventType.MENU_CLICK),
            position=(400, 200),
            text='GO TO MENU',
            text_colour=(255, 0, 0),
            font_size=50
        ),
        Text(
            event=CustomEvent.create_event(GameEventType.GAME_CLICK),
            position=(400, 400),
            text='NEW GAME',
            text_colour=(255, 0, 0),
            font_size=50
        )
    ],
    'menu': [
        Text(
            event=CustomEvent.create_event(MenuEventType.CONFIG_CLICK),
            position=(400, 200),
            text='START GAME',
            text_colour=(255, 0, 0),
            font_size=50
        ),
        Text(
            event=CustomEvent.create_event(MenuEventType.SETTINGS_CLICK),
            position=(400, 400),
            text='SETTINGS',
            text_colour=(255, 0, 0),
            font_size=50
        ),
    ],
    'settings': [
        Text(
            event=CustomEvent.create_event(SettingsEventType.MENU_CLICK),
            position=(400, 200),
            text='RETURN TO MAIN MENU',
            text_colour=(255, 0, 0),
            font_size=50
        ),
        Text(
            event=CustomEvent.create_event(SettingsEventType.UPDATE_PRIMARY),
            position=(400, 500),
            text='UPDATE PRIMARY COLOUR',
            text_colour=(255, 0, 0),
            font_size=50
        ),
    ],
    'config': [
        Text(
            event=CustomEvent.create_event(ConfigEventType.GAME_CLICK),
            position=(400, 200),
            text='START NEW GAME',
            text_colour=(255, 0, 0),
            font_size=50
        ),
        Text(
            event=CustomEvent.create_event(ConfigEventType.MENU_CLICK),
            position=(400, 300),
            text='RETURN TO MAIN MENU',
            text_colour=(255, 0, 0),
            font_size=50
        ),
    ]
}