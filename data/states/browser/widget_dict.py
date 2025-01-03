from data.components.custom_event import CustomEvent
from data.constants import BrowserEventType, GAMES_PER_PAGE
from data.assets import GRAPHICS
from data.widgets import *
from data.database.database_helpers import get_number_of_games

BROWSER_HEIGHT = 0.6

browser_strip = BrowserStrip(
    relative_position=(0.0, 0.0),
    relative_height=BROWSER_HEIGHT,
    games_list=[]
)

BROWSER_WIDGETS = {
    'default': [
        IconButton(
            relative_position=(0.075, 0.05),
            relative_size=(0.1, 0.1),
            scale_mode='height',
            margin=10,
            border_width=5,
            border_radius=5,
            fixed_width=True,
            anchor_x='right',
            icon=GRAPHICS['home'],
            event=CustomEvent(BrowserEventType.MENU_CLICK)
        ),
        IconButton(
            relative_position=(0.1, 0.8),
            relative_size=(0.1, 0.1),
            scale_mode='height',
            margin=10,
            border_width=5,
            border_radius=10,
            icon=GRAPHICS['copy'],
            event=CustomEvent(BrowserEventType.COPY_CLICK),
        ),
        IconButton(
            relative_position=(0.25, 0.8),
            relative_size=(0.1, 0.1),
            scale_mode='height',
            margin=10,
            border_width=5,
            border_radius=10,
            fill_colour=(255, 0, 0),
            icon=GRAPHICS['trash'],
            event=CustomEvent(BrowserEventType.DELETE_CLICK),
        ),
        IconButton(
            relative_position=(0.4, 0.8),
            relative_size=(0.1, 0.1),
            scale_mode='height',
            margin=10,
            border_width=5,
            border_radius=10,
            icon=GRAPHICS['review'],
            event=CustomEvent(BrowserEventType.REVIEW_CLICK),
        ),
        Text(
            relative_position=(0.4, 0.8),
            relative_size=(0.3, 0.075),
            text='SORT BY:',
            fill_colour=(0, 0, 0, 0),
            border_width=0,
            margin=0,
            text_colour=(255, 255, 255)
        )
    ],
    'browser_strip':
        browser_strip,
    'scroll_area':
    ScrollArea(
        relative_position=(0.0, 0.15),
        relative_size=(0.5, BROWSER_HEIGHT),
        vertical=False,
        widget=browser_strip
    ),
    'filter_column_dropdown':
    Dropdown(
        relative_position=(0.65, 0.8),
        relative_height=0.075,
        word_list=['moves', 'winner', 'time'],
        fill_colour=(255, 100, 100),
        event=CustomEvent(BrowserEventType.FILTER_COLUMN_CLICK)
    ),
    'filter_ascend_dropdown':
    Dropdown(
        relative_position=(0.85, 0.8),
        relative_height=0.075,
        word_list=['asc', 'desc'],
        fill_colour=(255, 100, 100),
        event=CustomEvent(BrowserEventType.FILTER_ASCEND_CLICK)
    )
}

number_of_pages = get_number_of_games() // GAMES_PER_PAGE + 1
carousel_widgets = {
    i: Text(
        relative_position=(0, 0),
        relative_size=(0.3, 0.1),
        text=f"PAGE {i} OF {number_of_pages}",
        fit_vertical=True,
        border_width=0,
    )
    for i in range(1, number_of_pages + 1)
}

BROWSER_WIDGETS['page_carousel'] = Carousel(
    relative_position = (0, 0.03),
    anchor_x='center',
    margin=5,
    border_width=0,
    widgets_dict=carousel_widgets,
    event=CustomEvent(BrowserEventType.PAGE_CLICK),
)