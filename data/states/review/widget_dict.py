import pygame
from data.widgets import *
from data.components.custom_event import CustomEvent
from data.constants import ReviewEventType
from data.assets import GRAPHICS

screen = pygame.display.get_surface()

info_container = Rectangle(
    relative_position=(0.35, 0),
    relative_size=(0.2, 0.3),
    anchor_x='center',
    anchor_y='center'
)

REVIEW_WIDGETS = {
    'default': [
        info_container,
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
    ),
    'move_number_text':
    Text(
        parent=info_container,
        relative_size=(0.9, 0.3),
        relative_position=(0.05, 0.65),
        border_width=0,
        fit_vertical=False,
        text='MOVE NO:',
    ),
    'move_colour_text':
    Text(
        parent=info_container,
        relative_size=(0.9, 0.3),
        relative_position=(0.05, 0.35),
        border_width=0,
        fit_vertical=False,
        text='TO MOVE',
    ),
    'winner_text':
    Text(
        parent=info_container,
        relative_size=(0.9, 0.3),
        relative_position=(0.05, 0.05),
        border_width=0,
        fit_vertical=False,
        text='WINNER:',
    ),
    'blue_timer':
    Timer(
        relative_position=(0.05, -0.05),
        anchor_y='center',
        relative_size=(0.1, 0.1),
    ),
    'red_timer':
    Timer(
        relative_position=(0.05, 0.05),
        anchor_y='center',
        relative_size=(0.1, 0.1),
    ),
    'timer_disabled_text':
    Text(
        relative_size=(0.2, 0.1),
        relative_position=(0.05, 0),
        anchor_y='center',
        fit_vertical=False,
        text='TIMER DISABLED',
    ),
}