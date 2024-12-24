from data.widgets import *
from data.components.custom_event import CustomEvent
from data.constants import GameEventType, RotationDirection, Colour
from data.assets import GRAPHICS

move_list = MoveList(
    relative_position=(0, 0),
    relative_width=0.2,
    minimum_height=390,
    fill_colour=(100, 100, 100),
    move_list=[]
)

resign_button = TextButton(
    relative_position=(0.125, 0.15),
    relative_size=(0.15, 0.1),
    fit_vertical=False,
    anchor_y='bottom',
    anchor_x='center',
    text="   Resign",
    margin=1,
    event=CustomEvent(GameEventType.RESIGN_CLICK)
)

draw_button = TextButton(
    relative_position=(-0.125, 0.15),
    relative_size=(0.15, 0.1),
    anchor_y='bottom',
    fit_vertical=False,
    anchor_x='center',
    text="   Draw",
    margin=1,
    event=CustomEvent(GameEventType.DRAW_CLICK)
)

GAME_WIDGETS = {
    'default': [
        IconButton(
            relative_position=(-0.025, 0.15),
            relative_size=(0.1, 0.1),
            anchor_y='bottom',
            anchor_x='center',
            margin=10,
            icon=GRAPHICS['clockwise_arrow'],
            scale_mode='height',
            event=CustomEvent(GameEventType.ROTATE_PIECE, rotation_direction=RotationDirection.CLOCKWISE)
        ),
        IconButton(
            relative_position=(0.025, 0.15),
            relative_size=(0.1, 0.1),
            anchor_y='bottom',
            anchor_x='center',
            margin=10,
            icon=GRAPHICS['anticlockwise_arrow'],
            scale_mode='height',
            event=CustomEvent(GameEventType.ROTATE_PIECE, rotation_direction=RotationDirection.ANTICLOCKWISE)
        ),
        resign_button,
        draw_button,
        Icon(
            parent=resign_button,
            relative_position=(0, 0),
            relative_size=(1, 1),
            fill_colour=(0, 0, 0, 0),
            scale_mode='height',
            border_radius=0,
            border_width=0,
            margin=10,
            icon=GRAPHICS['resign']
        ),
        Icon(
            parent=draw_button,
            relative_position=(0, 0),
            relative_size=(1, 1),
            fill_colour=(0, 0, 0, 0),
            scale_mode='height',
            border_radius=0,
            border_width=0,
            margin=10,
            icon=GRAPHICS['draw']
        ),
    ],
    'blue_timer':
    Timer(
        relative_position=(0.05, -0.05),
        anchor_y='center',
        relative_size=(0.1, 0.1),
        event=CustomEvent(GameEventType.TIMER_END, active_colour=Colour.BLUE),
    ),
    'red_timer':
    Timer(
        relative_position=(0.05, 0.05),
        anchor_y='center',
        relative_size=(0.1, 0.1),
        event=CustomEvent(GameEventType.TIMER_END, active_colour=Colour.RED),
    ),
    'status_text':
    Text(
        relative_position=(0, 0.05),
        relative_size=(0.4, 0.1),
        anchor_x='center',
        fit_vertical=False,
        margin=10,
        text="g",
        minimum_width=400
    ),
    'chessboard':
    Chessboard(
        relative_position=(0, 0),
        anchor_x='center',
        anchor_y='center',
        scale_mode='width',
        relative_width=0.4
    ),
    'move_list':
        move_list,
    'scroll_area':
    ScrollArea(
        relative_position=(0.25, 0),
        relative_size=(0.2, 0.4),
        anchor_x='right',
        anchor_y='center',
        vertical=True,
        widget=move_list
    )
}

PAUSE_WIDGETS = {
    'default': [
        TextButton(
            relative_position=(0, -0.1),
            relative_size=(0.3, 0.2),
            anchor_x='center',
            anchor_y='center',
            text='GO TO MENU',
            fit_vertical=False,
            text_colour=(255, 0, 0),
            event=CustomEvent(GameEventType.MENU_CLICK)
        ),
        TextButton(
            relative_position=(0, 0.1),
            relative_size=(0.3, 0.2),
            anchor_x='center',
            anchor_y='center',
            text='RESUME GAME',
            fit_vertical=False,
            text_colour=(255, 0, 0),
            event=CustomEvent(GameEventType.PAUSE_CLICK)
        )
    ]
}

win_container = Rectangle(
    relative_position=(0, 0),
    relative_size=(0.6, 0.6),
    scale_mode='height',
    anchor_x='center',
    anchor_y='center',
    fill_colour=(128, 128, 128, 200),
)

WIN_WIDGETS = {
    'default': [
        win_container,      
        TextButton(
            parent=win_container,
            relative_position=(0.45, 0.05),
            relative_size=(0.5, 0.4),
            text='GO TO MENU',
            fit_vertical=False,
            text_colour=(255, 0, 0),
            event=CustomEvent(GameEventType.MENU_CLICK)
        ),
        TextButton(
            parent=win_container,
            relative_position=(0.45, 0.55),
            relative_size=(0.5, 0.4),
            text='NEW GAME',
            fit_vertical=False,
            text_colour=(255, 0, 0),
            event=CustomEvent(GameEventType.GAME_CLICK)
        ),
    ],
    'blue_trophy':
    Icon(
        parent=win_container,
        relative_position=(0.05, 0.05),
        relative_size=(0.4, 0.9),
        border_width=0,
        margin=0,
        icon=GRAPHICS['blue_trophy'],
        fill_colour=(0, 0, 0, 0),
    ),
    'red_trophy':
    Icon(
        parent=win_container,
        relative_position=(0.05, 0.05),
        relative_size=(0.4, 0.9),
        border_width=0,
        margin=0,
        icon=GRAPHICS['red_trophy'],
        fill_colour=(0, 0, 0, 0),
    ),
    'draw_trophy':
    Icon(
        parent=win_container,
        relative_position=(0.05, 0.05),
        relative_size=(0.4, 0.9),
        border_width=0,
        margin=0,
        icon=GRAPHICS['hug'],
        fill_colour=(0, 0, 0, 0),
    )
}