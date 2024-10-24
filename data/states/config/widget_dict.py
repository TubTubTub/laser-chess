from data.components.widgets import *
from data.components.custom_event import CustomEvent
from data.constants import ConfigEventType

CONFIG_WIDGETS = {
    'default': [
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