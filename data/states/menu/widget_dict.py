from data.widgets import *
from data.components.custom_event import CustomEvent
from data.constants import MenuEventType
from data.assets import GRAPHICS

from data.theme import theme

MENU_WIDGETS = {
    'default': [
        Rectangle(
            relative_position=(0.1, 0.1),
            relative_size=(0.3, 0.3),
            fill_colour=(255, 0, 0),
            border_width=0,
        ),
        Rectangle(
            relative_position=(0.6, 0.6),
            relative_size=(0.3, 0.3),
            fill_colour=(255, 0, 0),
            border_width=0,
        ),
        Rectangle(
            relative_position=(0.3, 0.7),
            relative_size=(0.2, 0.2),
            fill_colour=(255, 0, 0),
            border_width=0,
        ),
        Rectangle(
            relative_position=(0.1, 0.5),
            relative_size=(0.2, 0.2),
            fill_colour=(255, 0, 0),
            border_width=0,
            border_radius=50,
        ),
        Rectangle(
            relative_position=(0.7, 0.3),
            relative_size=(0.2, 0.2),
            fill_colour=(255, 0, 0),
            border_width=0,
            border_radius=50,
        ),
        Rectangle(
            relative_position=(0.5, 0.1),
            relative_size=(0.2, 0.2),
            fill_colour=(255, 0, 0),
            border_width=0,
            border_radius=60,
        )
        # TextButton(
        #     relative_position=(0.0, 0.4),
        #     relative_size=(0.4, 0.1),
        #     text='START GAME',
        #     anchor_x='center',
        #     text_colour=theme['textPrimary'],
        #     margin=10,
        #     fill_colour=theme['fillPrimary'],
        #     event=CustomEvent(MenuEventType.CONFIG_CLICK)
        # ),
        # TextButton(
        #     relative_position=(0.0, 0.6),
        #     relative_size=(0.4, 0.1),
        #     text='SETTINGS',
        #     anchor_x='center',
        #     text_colour=theme['textPrimary'],
        #     margin=10,
        #     fill_colour=theme['fillPrimary'],
        #     event=CustomEvent(MenuEventType.SETTINGS_CLICK)
        # ),
        # TextButton(
        #     relative_position=(0.0, 0.8),
        #     relative_size=(0.4, 0.1),
        #     text='RECENT GAMES',
        #     anchor_x='center',
        #     text_colour=theme['textPrimary'],
        #     margin=10,
        #     fill_colour=theme['fillPrimary'],
        #     event=CustomEvent(MenuEventType.BROWSER_CLICK)
        # ),
        # Icon(
        #     relative_position=(0.0, 0.1),
        #     relative_size=(0.3, 0.2),
        #     anchor_x='center',
        #     fill_colour=theme['fillSecondary'],
        #     icon=GRAPHICS['title_screen_art'],
        #     stretch=False
        # ),
    ]
}