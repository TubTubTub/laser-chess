from data.widgets import *
from data.utils.enums import RotationDirection, Colour
from data.components.custom_event import CustomEvent
from data.utils.event_types import GameEventType
from data.utils.assets import GRAPHICS

right_container = Rectangle(
    relative_position=(0.05, 0),
    relative_size=(0.2, 0.5),
    anchor_y='center',
    anchor_x='right',
)

rotate_container = Rectangle(
    relative_position=(0, 0.05),
    relative_size=(0.2, 0.1),
    anchor_x='center',
    anchor_y='bottom',
)

move_list = MoveList(
    parent=right_container,
    relative_position=(0, 0),
    relative_width=1,
    minimum_height=300,
    move_list=[]
)

resign_button = TextButton(
    parent=right_container,
    relative_position=(0, 0),
    relative_size=(0.5, 0.2),
    fit_vertical=False,
    anchor_y='bottom',
    text="   Resign",
    margin=5,
    event=CustomEvent(GameEventType.RESIGN_CLICK)
)

draw_button = TextButton(
    parent=right_container,
    relative_position=(0, 0),
    relative_size=(0.5, 0.2),
    fit_vertical=False,
    anchor_x='right',
    anchor_y='bottom',
    text="   Draw",
    margin=5,
    event=CustomEvent(GameEventType.DRAW_CLICK)
)

top_right_container = Rectangle(
    relative_position=(0, 0),
    relative_size=(0.225, 0.075),
    fixed_position=(5, 5),
    anchor_x='right',
    scale_mode='height'
)

GAME_WIDGETS = {
    'help':
    Icon(
        relative_position=(0, 0),
        relative_size=(1.02, 1.02),
        icon=GRAPHICS['game_help'],
        anchor_x='center',
        anchor_y='center',
        border_width=0,
        fill_colour=(0, 0, 0, 0)
    ),
    'tutorial':
    Icon(
        relative_position=(0, 0),
        relative_size=(0.9, 0.9),
        icon=GRAPHICS['game_tutorial'],
        anchor_x='center',
        anchor_y='center',
    ),
    'default': [
        right_container,
        rotate_container,
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
            event=CustomEvent(GameEventType.MENU_CLICK)
        ),
        ReactiveIconButton(
            parent=top_right_container,
            relative_position=(0, 0),
            relative_size=(1, 1),
            scale_mode='height',
            base_icon=GRAPHICS['tutorial_base'],
            hover_icon=GRAPHICS['tutorial_hover'],
            press_icon=GRAPHICS['tutorial_press'],
            event=CustomEvent(GameEventType.TUTORIAL_CLICK)
        ),
        ReactiveIconButton(
            parent=top_right_container,
            relative_position=(0.33, 0),
            relative_size=(1, 1),
            scale_mode='height',
            base_icon=GRAPHICS['help_base'],
            hover_icon=GRAPHICS['help_hover'],
            press_icon=GRAPHICS['help_press'],
            event=CustomEvent(GameEventType.HELP_CLICK)
        ),
        ReactiveIconButton(
            parent=rotate_container,
            relative_position=(0, 0),
            relative_size=(1, 1),
            scale_mode='height',
            anchor_x='right',
            base_icon=GRAPHICS['clockwise_arrow_base'],
            hover_icon=GRAPHICS['clockwise_arrow_hover'],
            press_icon=GRAPHICS['clockwise_arrow_press'],
            event=CustomEvent(GameEventType.ROTATE_PIECE, rotation_direction=RotationDirection.CLOCKWISE)
        ),
        ReactiveIconButton(
            parent=rotate_container,
            relative_position=(0, 0),
            relative_size=(1, 1),
            scale_mode='height',
            base_icon=GRAPHICS['anticlockwise_arrow_base'],
            hover_icon=GRAPHICS['anticlockwise_arrow_hover'],
            press_icon=GRAPHICS['anticlockwise_arrow_press'],
            event=CustomEvent(GameEventType.ROTATE_PIECE, rotation_direction=RotationDirection.ANTICLOCKWISE)
        ),
        resign_button,
        draw_button,
        Icon(
            parent=resign_button,
            relative_position=(0, 0),
            relative_size=(0.75, 0.75),
            fill_colour=(0, 0, 0, 0),
            scale_mode='height',
            anchor_y='center',
            border_radius=0,
            border_width=0,
            margin=5,
            icon=GRAPHICS['resign']
        ),
        Icon(
            parent=draw_button,
            relative_position=(0, 0),
            relative_size=(0.75, 0.75),
            fill_colour=(0, 0, 0, 0),
            scale_mode='height',
            anchor_y='center',
            border_radius=0,
            border_width=0,
            margin=5,
            icon=GRAPHICS['draw']
        ),
    ],
    'scroll_area': # REMEMBER SCROLL AREA AFTER CONTAINER FOR RESIZING
    ScrollArea(
        parent=right_container,
        relative_position=(0, 0),
        relative_size=(1, 0.8),
        vertical=True,
        widget=move_list
    ),
    'move_list':
        move_list,
    'blue_timer':
    Timer(
        relative_position=(0.05, 0.05),
        anchor_y='center',
        relative_size=(0.1, 0.1),
        active_colour=Colour.BLUE,
        event=CustomEvent(GameEventType.TIMER_END),
    ),
    'red_timer':
    Timer(
        relative_position=(0.05, -0.05),
        anchor_y='center',
        relative_size=(0.1, 0.1),
        active_colour=Colour.RED,
        event=CustomEvent(GameEventType.TIMER_END),
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
    )
}

PAUSE_WIDGETS = {
    'default': [
        TextButton(
            relative_position=(0, -0.125),
            relative_size=(0.3, 0.2),
            anchor_x='center',
            anchor_y='center',
            text='GO TO MENU',
            fit_vertical=False,
            event=CustomEvent(GameEventType.MENU_CLICK)
        ),
        TextButton(
            relative_position=(0, 0.125),
            relative_size=(0.3, 0.2),
            anchor_x='center',
            anchor_y='center',
            text='RESUME GAME',
            fit_vertical=False,
            event=CustomEvent(GameEventType.PAUSE_CLICK)
        )
    ]
}

win_container = Rectangle(
    relative_position=(0, 0),
    relative_size=(0.4, 0.8),
    scale_mode='height',
    anchor_x='center',
    anchor_y='center',
    fill_colour=(128, 128, 128, 200),
    visible=True
)

WIN_WIDGETS = {
    'default': [
        win_container,
        TextButton(
            parent=win_container,
            relative_position=(0, 0.5),
            relative_size=(0.8, 0.15),
            text='GO TO MENU',
            anchor_x='center',
            fit_vertical=False,
            event=CustomEvent(GameEventType.MENU_CLICK)
        ),
        TextButton(
            parent=win_container,
            relative_position=(0, 0.65),
            relative_size=(0.8, 0.15),
            text='REVIEW GAME',
            anchor_x='center',
            fit_vertical=False,
            event=CustomEvent(GameEventType.REVIEW_CLICK)
        ),
        TextButton(
            parent=win_container,
            relative_position=(0, 0.8),
            relative_size=(0.8, 0.15),
            text='NEW GAME',
            anchor_x='center',
            fit_vertical=False,
            event=CustomEvent(GameEventType.GAME_CLICK)
        ),
    ],
    'blue_won':
    Icon(
        parent=win_container,
        relative_position=(0, 0.05),
        relative_size=(0.8, 0.3),
        anchor_x='center',
        border_width=0,
        margin=0,
        icon=GRAPHICS['blue_won'],
        fill_colour=(0, 0, 0, 0),
    ),
    'red_won':
    Icon(
        parent=win_container,
        relative_position=(0, 0.05),
        relative_size=(0.8, 0.3),
        anchor_x='center',
        border_width=0,
        margin=0,
        icon=GRAPHICS['red_won'],
        fill_colour=(0, 0, 0, 0),
        fit_icon=True,
    ),
    'draw_won':
    Icon(
        parent=win_container,
        relative_position=(0, 0.05),
        relative_size=(0.8, 0.3),
        anchor_x='center',
        border_width=0,
        margin=0,
        icon=GRAPHICS['draw_won'],
        fill_colour=(0, 0, 0, 0),
    ),
    'by_checkmate':
    Icon(
        parent=win_container,
        relative_position=(0, 0.375),
        relative_size=(0.8, 0.1),
        anchor_x='center',
        border_width=0,
        margin=0,
        icon=GRAPHICS['by_checkmate'],
        fill_colour=(0, 0, 0, 0),
    ),
    'by_resignation':
    Icon(
        parent=win_container,
        relative_position=(0, 0.375),
        relative_size=(0.8, 0.1),
        anchor_x='center',
        border_width=0,
        margin=0,
        icon=GRAPHICS['by_resignation'],
        fill_colour=(0, 0, 0, 0),
    ),
    'by_draw':
    Icon(
        parent=win_container,
        relative_position=(0, 0.375),
        relative_size=(0.8, 0.1),
        anchor_x='center',
        border_width=0,
        margin=0,
        icon=GRAPHICS['by_draw'],
        fill_colour=(0, 0, 0, 0),
    ),
    'by_timeout':
    Icon(
        parent=win_container,
        relative_position=(0, 0.375),
        relative_size=(0.8, 0.1),
        anchor_x='center',
        border_width=0,
        margin=0,
        icon=GRAPHICS['by_timeout'],
        fill_colour=(0, 0, 0, 0),
    )
}