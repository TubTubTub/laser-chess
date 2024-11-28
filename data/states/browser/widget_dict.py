from data.widgets import *
from data.components.custom_event import CustomEvent
from data.constants import BrowserEventType
from data.assets import GRAPHICS

from data.theme import theme

browser_strip = BrowserStrip(
    relative_position=(0.0, 0.0),
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
            relative_position=(0.4, 0.78),
            size=(100, 100),
            margin=10,
            border_width=5,
            border_radius=10,
            icon=GRAPHICS['copy'],
            event=CustomEvent(BrowserEventType.COPY_CLICK),
        ),
        IconButton(
            relative_position=(0.55, 0.78),
            size=(100, 100),
            margin=10,
            border_width=5,
            border_radius=10,
            fill_colour=(255, 0, 0),
            icon=GRAPHICS['trash'],
            event=CustomEvent(BrowserEventType.DELETE_CLICK),
        ),
        Text(
            relative_position=(0.74, 0.75),
            text='FILTER BY:',
            fill_colour=(0, 0, 0, 0),
            font_size=30,
            text_colour=(255, 255, 255)
        )
    ],
    'browser_strip':
        browser_strip,
    'scroll_area':
    ScrollArea(
        relative_position=(0.0, 0.15),
        size=(1000, 350),
        vertical=False,
        widget=browser_strip
    ),
    'filter_column_dropdown':
    Dropdown(
        relative_position=(0.87,0.77),
        word_list=['moves', 'winner', 'time'],
        font_size=25,
        fill_colour=(255, 100, 100),
        event=CustomEvent(BrowserEventType.FILTER_COLUMN_CLICK)
    ),
    'filter_ascend_dropdown':
    Dropdown(
        relative_position=(0.87, 0.87),
        word_list=['asc', 'desc'],
        font_size=25,
        fill_colour=(255, 100, 100),
        event=CustomEvent(BrowserEventType.FILTER_ASCEND_CLICK)
    )
}