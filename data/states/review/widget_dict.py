from data.widgets import *
from data.components.custom_event import CustomEvent
from data.constants import ReviewEventType, Colour
from data.assets import GRAPHICS

MOVE_LIST_WIDTH = 0.2

right_container = Rectangle(
    relative_position=(0.05, 0),
    relative_size=(0.2, 0.7),
    anchor_y='center',
    anchor_x='right'
)

info_container = Rectangle(
    parent=right_container,
    relative_position=(0, 0.5),
    relative_size=(1, 0.5),
    visible=True
)

arrow_container = Rectangle(
    relative_position=(0, 0.05),
    relative_size=(0.4, 0.1),
    anchor_x='center',
    anchor_y='bottom'
)

move_list = MoveList(
    parent=right_container,
    relative_position=(0, 0),
    relative_width=1,
    minimum_height=300,
    move_list=[]
)

top_right_container = Rectangle(
    relative_position=(0, 0),
    relative_size=(0.15, 0.075),
    fixed_position=(5, 5),
    anchor_x='right',
    scale_mode='height'
)

REVIEW_WIDGETS = {
    'help':
    Icon(
        relative_position=(0, 0),
        relative_size=(1.02, 1.02),
        icon=GRAPHICS['review_help'],
        anchor_x='center',
        anchor_y='center',
        border_width=0,
        fill_colour=(0, 0, 0, 0)
    ),
    'default': [
        arrow_container,
        right_container,
        info_container,
        top_right_container,
        ReactiveIconButton(
            parent=top_right_container,
            relative_position=(0, 0),
            relative_size=(1, 1),
            anchor_x='right',
            scale_mode='height',
            base_icon=GRAPHICS['home_base'],
            hover_icon=GRAPHICS['home_hover'],
            press_icon=GRAPHICS['home_press'],
            event=CustomEvent(ReviewEventType.MENU_CLICK)
        ),
        ReactiveIconButton(
            parent=top_right_container,
            relative_position=(0, 0),
            relative_size=(1, 1),
            scale_mode='height',
            base_icon=GRAPHICS['help_base'],
            hover_icon=GRAPHICS['help_hover'],
            press_icon=GRAPHICS['help_press'],
            event=CustomEvent(ReviewEventType.HELP_CLICK)
        ),
        ReactiveIconButton(
            parent=arrow_container,
            relative_position=(0, 0),
            relative_size=(1, 1),
            scale_mode='height',
            base_icon=GRAPHICS['left_arrow_filled_base'],
            hover_icon=GRAPHICS['left_arrow_filled_hover'],
            press_icon=GRAPHICS['left_arrow_filled_press'],
            event=CustomEvent(ReviewEventType.PREVIOUS_CLICK)
        ),
        ReactiveIconButton(
            parent=arrow_container,
            relative_position=(0, 0),
            relative_size=(1, 1),
            scale_mode='height',
            anchor_x='right',
            base_icon=GRAPHICS['right_arrow_filled_base'],
            hover_icon=GRAPHICS['right_arrow_filled_hover'],
            press_icon=GRAPHICS['right_arrow_filled_press'],
            event=CustomEvent(ReviewEventType.NEXT_CLICK)
        ),
    ],
    'move_list':
        move_list,
    'scroll_area':
    ScrollArea(
        parent=right_container,
        relative_position=(0, 0),
        relative_size=(1, 0.5),
        vertical=True,
        widget=move_list
    ),
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
        relative_position=(0, 0),
        relative_size=(1, 0.3),
        anchor_y='bottom',
        text='MOVE NO:',
        fit_vertical=False,
        margin=10,
        border_width=0,
        fill_colour=(0, 0, 0, 0),
    ),
    'move_colour_text':
    Text(
        parent=info_container,
        relative_size=(1, 0.3),
        relative_position=(0, 0),
        anchor_y='center',
        text='TO MOVE',
        fit_vertical=False,
        margin=10,
        border_width=0,
        fill_colour=(0, 0, 0, 0),
    ),
    'winner_text':
    Text(
        parent=info_container,
        relative_size=(1, 0.3),
        relative_position=(0, 0),
        text='WINNER:',
        fit_vertical=False,
        margin=10,
        border_width=0,
        fill_colour=(0, 0, 0, 0),
    ),
    'blue_timer':
    Timer(
        relative_position=(0.05, 0.05),
        anchor_y='center',
        relative_size=(0.1, 0.1),
        active_colour=Colour.BLUE,
    ),
    'red_timer':
    Timer(
        relative_position=(0.05, -0.05),
        anchor_y='center',
        relative_size=(0.1, 0.1),
        active_colour=Colour.RED
    ),
    'timer_disabled_text':
    Text(
        relative_size=(0.2, 0.1),
        relative_position=(0.05, 0),
        anchor_y='center',
        fit_vertical=False,
        text='TIMER DISABLED',
    ),
    'blue_piece_display':
    PieceDisplay(
        relative_position=(0.05, 0.05),
        relative_size=(0.2, 0.1),
        anchor_y='bottom',
        active_colour=Colour.BLUE
    ),
    'red_piece_display':
    PieceDisplay(
        relative_position=(0.05, 0.05),
        relative_size=(0.2, 0.1),
        active_colour=Colour.RED
    ),
}