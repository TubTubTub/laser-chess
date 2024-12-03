from data.widgets import *
from data.components.custom_event import CustomEvent
from data.constants import BrowserEventType
from data.assets import GRAPHICS

from data.theme import theme

browser_strip = BrowserStrip(
    relative_position=(0.0, 0.0),
    relative_item_width=0.3,
    games_list=[]
)

BROWSER_WIDGETS = {
    'default': [
        IconButton(
            relative_position=(0.92, 0.02),
            relative_size=(0.3, 0.3),
            margin=10,
            border_width=5,
            border_radius=5,
            icon=GRAPHICS['home'],
            event=CustomEvent(BrowserEventType.MENU_CLICK)
        ),
        IconButton(
            relative_position=(0.4, 0.78),
            relative_size=(0.3, 0.3),
            margin=10,
            border_width=5,
            border_radius=10,
            icon=GRAPHICS['copy'],
            event=CustomEvent(BrowserEventType.COPY_CLICK),
        ),
        IconButton(
            relative_position=(0.55, 0.78),
            relative_size=(0.3, 0.3),
            margin=10,
            border_width=5,
            border_radius=10,
            fill_colour=(255, 0, 0),
            icon=GRAPHICS['trash'],
            event=CustomEvent(BrowserEventType.DELETE_CLICK),
        ),
        Text(
            relative_position=(0.75, 0.75),
            relative_size=(0.3, 0.3),
            text='SORT BY:',
            fill_colour=(0, 0, 0, 0),
            text_colour=(255, 255, 255)
        )
    ],
    'browser_strip':
        browser_strip,
    'scroll_area':
    ScrollArea(
        relative_position=(0.0, 0.15),
        relative_size=(1, 0.5),
        vertical=False,
        widget=browser_strip
    ),
    'filter_column_dropdown':
    Dropdown(
        relative_position=(0.87,0.77),
        relative_size=(0.3, 0.3),
        word_list=['moves', 'winner', 'time'],
        fill_colour=(255, 100, 100),
        event=CustomEvent(BrowserEventType.FILTER_COLUMN_CLICK)
    ),
    'filter_ascend_dropdown':
    Dropdown(
        relative_position=(0.87, 0.87),
        relative_size=(0.3, 0.3),
        word_list=['asc', 'desc'],
        fill_colour=(255, 100, 100),
        event=CustomEvent(BrowserEventType.FILTER_ASCEND_CLICK)
    )
}