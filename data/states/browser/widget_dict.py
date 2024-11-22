from data.widgets import *
from data.components.custom_event import CustomEvent
from data.constants import BrowserEventType
from data.assets import GRAPHICS

from data.theme import theme

board_thumbnail_strip = BoardThumbnailStrip(
    relative_position=(0.5, 0),
    board_width=300,
    fen_string_list=[]
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
    ],
    'board_thumbnail_strip':
        board_thumbnail_strip,
    'scroll_area':
    ScrollArea(
        relative_position=(0.0, 0.3),
        size=(1000, 400),
        vertical=False,
        widget=board_thumbnail_strip
    )
}