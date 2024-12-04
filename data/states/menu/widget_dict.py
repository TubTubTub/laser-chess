from data.widgets import *
from data.components.custom_event import CustomEvent
from data.constants import MenuEventType
from data.assets import GRAPHICS

from data.theme import theme

MENU_WIDGETS = {
    'default': [
        TextButton(
            relative_position=(0.3, 0.4),
            relative_size=(0.4, 0.1),
            text='START GAME',
            text_colour=theme['textPrimary'],
            margin=10,
            fill_colour=theme['fillPrimary'],
            event=CustomEvent(MenuEventType.CONFIG_CLICK)
        ),
        TextButton(
            relative_position=(0.3, 0.6),
            relative_size=(0.4, 0.1),
            text='SETTINGS',
            text_colour=theme['textPrimary'],
            margin=10,
            fill_colour=theme['fillPrimary'],
            event=CustomEvent(MenuEventType.SETTINGS_CLICK)
        ),
        TextButton(
            relative_position=(0.3, 0.8),
            relative_size=(0.4, 0.1),
            text='RECENT GAMES',
            text_colour=theme['textPrimary'],
            margin=10,
            fill_colour=theme['fillPrimary'],
            event=CustomEvent(MenuEventType.BROWSER_CLICK)
        ),
        Icon(
            relative_position=(0.35, 0.1),
            relative_size=(0.3, 0.2),
            fill_colour=theme['fillSecondary'],
            icon=GRAPHICS['title_screen_art'],
            stretch=False
        ),
    ]
}