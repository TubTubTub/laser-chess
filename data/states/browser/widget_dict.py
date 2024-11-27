from data.widgets import *
from data.components.custom_event import CustomEvent
from data.constants import BrowserEventType
from data.assets import GRAPHICS

from data.theme import theme

browser_strip = BrowserStrip(
    relative_position=(0, 0),
    item_width=220,
    games_list=[]
)

BROWSER_WIDGETS = {
    'default': [
        IconButton(
            relative_position=(0.92, 0.02),
            size=(50, 50),
            margin=10,
            border_width=5,
            border_radius=5,
            icon=GRAPHICS['home'],
            event=CustomEvent(BrowserEventType.MENU_CLICK)
        ),
        IconButton(
            relative_position=(0.3, 0.1),
            size=(50, 50),
            margin=10,
            border_width=5,
            border_radius=10,
            icon=GRAPHICS['copy'],
            event=CustomEvent(BrowserEventType.COPY_CLICK),
        )
    ],
    'browser_strip':
        browser_strip,
    'scroll_area':
    ScrollArea(
        relative_position=(0.0, 0.3),
        size=(1000, 400),
        vertical=False,
        widget=browser_strip
    )
}