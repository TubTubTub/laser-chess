from data.widgets import *
from data.components.custom_event import CustomEvent
from data.constants import MenuEventType
from data.assets import GRAPHICS

MENU_WIDGETS = {
    'default': [
        TextButton(
            relative_position=(0.375, 0.5),
            text='START GAME',
            text_colour=(255, 0, 0),
            margin=50,
            font_size=50,
            fill_colour=(255, 255, 0),
            border_width=5,
            event=CustomEvent(MenuEventType.CONFIG_CLICK)
        ),
        TextButton(
            relative_position=(0.4, 0.7),
            text='SETTINGS',
            text_colour=(255, 0, 0),
            margin=50,
            font_size=50,
            fill_colour=(0, 0, 255),
            event=CustomEvent(MenuEventType.SETTINGS_CLICK)
        ),
        Icon(
            relative_position=(0.3, 0.1),
            size=(400, 200),
            fill_colour=(100, 100, 100, 255),
            icon=GRAPHICS['title_screen_art'],
        ),
        ScrollArea(
            relative_position=(0.1, 0.1),
            size=(200, 400),
            widget=Text(
                relative_position=(0, 0),
                text='hello',
                font_size=30
            )
        ),
    ]
}