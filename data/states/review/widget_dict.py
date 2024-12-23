import pygame
from data.widgets import *
from data.components.custom_event import CustomEvent
from data.constants import ReviewEventType
from data.assets import GRAPHICS

screen = pygame.display.get_surface()

REVIEW_WIDGETS = {
    'default': [
        IconButton(
            relative_position=(0.1, 0.02),
            relative_size=(0.05, 0.1),
            icon=GRAPHICS['home'],
            border_width=5,
            border_radius=5,
            margin=10,
            anchor_x='right',
            fixed_position=True,
            event=CustomEvent(ReviewEventType.MENU_CLICK)
        ),
        IconButton(
            relative_position=(-0.15, 0.15),
            relative_size=(0.1, 0.1),
            fill_colour=(0, 0, 0),
            anchor_y='bottom',
            anchor_x='center',
            margin=10,
            icon=GRAPHICS['back'],
            scale_mode='height',
            event=CustomEvent(ReviewEventType.PREVIOUS_CLICK)
        ),
        IconButton(
            relative_position=(0.15, 0.15),
            relative_size=(0.1, 0.1),
            fill_colour=(0, 0, 0),
            anchor_y='bottom',
            anchor_x='center',
            margin=10,
            icon=GRAPHICS['next'],
            scale_mode='height',
            event=CustomEvent(ReviewEventType.NEXT_CLICK)
        ),
    ],
    'chessboard':
    Chessboard(
        relative_position=(0, 0),
        relative_width=0.4,
        scale_mode='width',
        anchor_x='center',
        anchor_y='center'
    )
}