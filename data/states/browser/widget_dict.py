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

number_of_pages = get_number_of_games() // GAMES_PER_PAGE + 1

carousel_widgets = {
    i: Text(
        relative_position=(0, 0),
        relative_size=(0.3, 0.1),
        text=f"PAGE {i} OF {number_of_pages}",
        fill_colour=(0, 0, 0, 0),
        fit_vertical=True,
        border_width=0,
    )
    for i in range(1, number_of_pages + 1)
}

sort_by_container = Rectangle(
    relative_size=(0.5, 0.1),
    relative_position=(0.01, 0.75),
    anchor_x='right',
    visible=True
)

buttons_container = Rectangle(
    relative_position=(0, 0.025),
    relative_size=(0.5, 0.1),
    scale_mode='height',
    anchor_x='center'
)

BROWSER_WIDGETS = {
    'default': [
        buttons_container,
        sort_by_container,
        IconButton(
            relative_position=(0, 0),
            fixed_position=(5, 5),
            relative_size=(0.075, 0.075),
            icon=GRAPHICS['home'],
            scale_mode='height',
            margin=10,
            anchor_x='right',
            event=CustomEvent(BrowserEventType.MENU_CLICK)
        ),
        IconButton(
            parent=buttons_container,
            relative_position=(0, 0),
            relative_size=(1, 1),
            scale_mode='height',
            icon=GRAPHICS['copy'],
            margin=10,
            event=CustomEvent(BrowserEventType.COPY_CLICK),
        ),
        IconButton(
            parent=buttons_container,
            relative_position=(0, 0),
            relative_size=(1, 1),
            scale_mode='height',
            anchor_x='center',
            fill_colour=(255, 0, 0),
            margin=10,
            icon=GRAPHICS['trash'],
            event=CustomEvent(BrowserEventType.DELETE_CLICK),
        ),
        IconButton(
            parent=buttons_container,
            relative_position=(0, 0),
            relative_size=(1, 1),
            scale_mode='height',
            anchor_x='right',
            margin=10,
            icon=GRAPHICS['review'],
            event=CustomEvent(BrowserEventType.REVIEW_CLICK),
        ),
        Text(
            parent=sort_by_container,
            relative_position=(-1, 0),
            relative_size=(0.3, 1),
            fit_vertical=False,
            text='SORT BY:',
            border_width=0,
            margin=0,
            fill_colour=(0, 0, 0, 0),
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
        parent=sort_by_container,
        relative_position=(1.25, 0),
        relative_height=0.75,
        anchor_x='right',
        anchor_y='center',
        word_list=['time', 'moves', 'winner'],
        fill_colour=(255, 100, 100),
        event=CustomEvent(BrowserEventType.FILTER_COLUMN_CLICK)
    ),
    'filter_ascend_dropdown':
    Dropdown(
        parent=sort_by_container,
        relative_position=(1, 0),
        relative_height=0.75,
        anchor_x='right',
        anchor_y='center',
        word_list=['desc', 'asc'],
        fill_colour=(255, 100, 100),
        event=CustomEvent(BrowserEventType.FILTER_ASCEND_CLICK)
    ),
    'page_carousel':
    Carousel(
        relative_position=(0.01, 0.75),
        margin=5,
        border_width=0,
        fill_colour=(0, 0, 0, 0),
        widgets_dict=carousel_widgets,
        event=CustomEvent(BrowserEventType.PAGE_CLICK),
    )
}