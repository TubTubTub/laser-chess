from data.widgets import *
from data.components.custom_event import CustomEvent
from data.constants import MenuEventType, WidgetState
from data.assets import GRAPHICS

from data.managers.theme import theme

MENU_WIDGETS = {
    'default': [
        ReactiveTextButton(
            relative_position=(0.05, -0.2),
            relative_size=(0.15, 0.15),
            fill_colour=(0, 0, 0, 0),
            anchor_y='center',
            text='PLAY',
            center=True,
            text_center=False,
            event=CustomEvent(MenuEventType.CONFIG_CLICK)
        ),
        ReactiveTextButton(
            relative_position=(0.05, 0),
            relative_size=(0.3, 0.15),
            anchor_y='center',
            fill_colour=(0, 0, 0, 0),
            text='SETTINGS',
            center=True,
            text_center=False,
            event=CustomEvent(MenuEventType.SETTINGS_CLICK)
        ),
        ReactiveTextButton(
            relative_position=(0.05, 0.2),
            fill_colour=(0, 0, 0, 0),
            relative_size=(0.5, 0.15),
            anchor_y='center',
            text='RECENT GAMES',
            center=True,
            text_center=False,
            event=CustomEvent(MenuEventType.BROWSER_CLICK)
        ),
        Icon(
            relative_position=(0.0, 0.1),
            relative_size=(0.3, 0.2),
            anchor_x='center',
            fill_colour=theme['fillSecondary'],
            icon=GRAPHICS['title_screen_art'],
            stretch=False
        ),
    ]
}