import pygame
from data.widgets import *
from data.states.config.default_config import default_config
from data.components.custom_event import CustomEvent
from data.constants import ConfigEventType, Colour
from data.assets import GRAPHICS
from data.utils.asset_helpers import get_highlighted_icon
from data.managers.theme import theme

def float_validator(num_string):
    try:
        float(num_string)
        return True
    except:
        return False

if default_config['CPU_ENABLED']:
    pvp_icons = {False: GRAPHICS['swords'], True: GRAPHICS['swords']}
    pvc_icons = {True: GRAPHICS['robot'], False: GRAPHICS['robot']}
    pvc_locked = True
    pvp_locked = False
else:
    pvp_icons = {True: GRAPHICS['swords'], False: GRAPHICS['swords']}
    pvc_icons = {False: GRAPHICS['robot'], True: GRAPHICS['robot']}
    pvc_locked = False
    pvp_locked = True

if default_config['TIME_ENABLED']:
    time_enabled_icons = {True: GRAPHICS['timer'], False: get_highlighted_icon(GRAPHICS['timer'])}
else:
    time_enabled_icons = {False: get_highlighted_icon(GRAPHICS['timer']), True: GRAPHICS['timer']}

if default_config['COLOUR'] == Colour.BLUE:
    colour_icons = {Colour.BLUE: GRAPHICS['pharoah_0_a'], Colour.RED: GRAPHICS['pharoah_1_a']}
else:
    colour_icons = {Colour.RED: GRAPHICS['pharoah_1_a'], Colour.BLUE: GRAPHICS['pharoah_0_a']}

preview_container = Rectangle(
    relative_position=(-0.15, 0),
    relative_size=(0.65, 0.9),
    anchor_x='center',
    anchor_y='center',
)

config_container = Rectangle(
    relative_position=(0.325, 0),
    relative_size=(0.3, 0.9),
    anchor_x='center',
    anchor_y='center',
)

to_move_container = Rectangle(
    parent=config_container,
    relative_size=(0.9, 0.15),
    relative_position=(0, 0.1),
    anchor_x='center'
)

board_thumbnail = BoardThumbnail(
    parent=preview_container,
    relative_position=(0, 0),
    relative_width=0.7,
    scale_mode='width',
    anchor_x='right',
)

top_right_container = Rectangle(
    relative_position=(0, 0),
    relative_size=(0.15, 0.075),
    fixed_position=(5, 5),
    anchor_x='right',
    scale_mode='height'
)

CONFIG_WIDGETS = {
    'help':
    Icon(
        relative_position=(0, 0),
        relative_size=(0.9, 0.9),
        icon=GRAPHICS['temp_background'],
        anchor_x='center',
        anchor_y='center'
    ),
    'board_thumbnail':
        board_thumbnail,
    'default': [
        preview_container,
        config_container,
        to_move_container,
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
            event=CustomEvent(ConfigEventType.MENU_CLICK)
        ),
        ReactiveIconButton(
            parent=top_right_container,
            relative_position=(0, 0),
            relative_size=(1, 1),
            scale_mode='height',
            base_icon=GRAPHICS['help_base'],
            hover_icon=GRAPHICS['help_hover'],
            press_icon=GRAPHICS['help_press'],
            event=CustomEvent(ConfigEventType.HELP_CLICK)
        ),
        TextInput(
            parent=config_container,
            relative_position=(0.3, 0.3),
            relative_size=(0.65, 0.15),
            fit_vertical=True,
            placeholder='TIME CONTROL (DEFAULT 5)',
            default=str(default_config['TIME']),
            border_width=5,
            margin=20,
            validator=float_validator,
            event=CustomEvent(ConfigEventType.TIME_TYPE)
        ),
        Text(
            parent=config_container,
            fit_vertical=False,
            relative_position=(0.75, 0.3),
            relative_size=(0.2, 0.15),
            text='MINS',
            border_width=0,
            fill_colour=(0, 0, 0, 0)
        ),
        TextButton(
            parent=preview_container,
            relative_position=(0.3, 0),
            relative_size=(0.15, 0.15),
            text='CUSTOM',
            anchor_y='bottom',
            fit_vertical=False,
            margin=10,
            event=CustomEvent(ConfigEventType.SETUP_CLICK)
        )
    ],
    'fen_string_input':
    TextInput(
        parent=preview_container,
        relative_position=(0, 0),
        relative_size=(0.55, 0.15),
        fit_vertical=False,
        placeholder='ENTER FEN STRING',
        default='sc3ncfancpb2/2pc7/3Pd7/pa1Pc1rbra1pb1Pd/pb1Pd1RaRb1pa1Pc/6pb3/7Pa2/2PdNaFaNa3Sa b',
        border_width=5,
        anchor_y='bottom',
        anchor_x='right',
        margin=20,
        event=CustomEvent(ConfigEventType.FEN_STRING_TYPE)
    ),
    'start_button':
    TextButton(
        parent=config_container,
        relative_position=(0, 0),
        relative_size=(0.9, 0.3),
        anchor_y='bottom',
        anchor_x='center',
        text='START NEW GAME',
        strength=0.1,
        text_colour=theme['textSecondary'],
        margin=20,
        fit_vertical=False,
        event=CustomEvent(ConfigEventType.GAME_CLICK)
    ),
    'timer_button':
    MultipleIconButton(
        parent=config_container,
        scale_mode='height',
        relative_position=(0.05, 0.3),
        relative_size=(0.15, 0.15),
        margin=10,
        border_width=5,
        border_radius=5,
        icons_dict=time_enabled_icons,
        event=CustomEvent(ConfigEventType.TIME_CLICK)
    ),
    'pvp_button':
    MultipleIconButton(
        parent=config_container,
        relative_position=(-0.225, 0.5),
        relative_size=(0.45, 0.15),
        margin=15,
        anchor_x='center',
        icons_dict=pvp_icons,
        stretch=False,
        event=CustomEvent(ConfigEventType.PVP_CLICK)
    ),
    'pvc_button':
    MultipleIconButton(
        parent=config_container,
        relative_position=(0.225, 0.5),
        relative_size=(0.45, 0.15),
        anchor_x='center',
        margin=15,
        icons_dict=pvc_icons,
        stretch=False,
        event=CustomEvent(ConfigEventType.PVC_CLICK)
    ),
    'invalid_fen_string':
    Text(
        parent=board_thumbnail,
        relative_position=(0, 0),
        relative_size=(0.9, 0.1),
        fit_vertical=False,
        anchor_x='center',
        anchor_y='center',
        text='INVALID FEN STRING!',
        margin=10,
        fill_colour=theme['fillError'],
        text_colour=theme['textError'],
    ),
    'preset_1':
    BoardThumbnailButton(
        parent=preview_container,
        relative_width=0.25,
        relative_position=(0, 0),
        scale_mode='width',
        fen_string="sc3ncfancpb2/2pc7/3Pd6/pa1Pc1rbra1pb1Pd/pb1Pd1RaRb1pa1Pc/6pb3/7Pa2/2PdNaFaNa3Sa b",
        event=CustomEvent(ConfigEventType.PRESET_CLICK)
    ),
    'preset_2':
    BoardThumbnailButton(
        parent=preview_container,
        relative_width=0.25,
        relative_position=(0, 0.35),
        scale_mode='width',
        fen_string="sc3ncfcncra2/10/3Pd2pa3/paPc2Pbra2pbPd/pbPd2Rapd2paPc/3Pc2pb3/10/2RaNaFaNa3Sa b",
        event=CustomEvent(ConfigEventType.PRESET_CLICK)
    ),
    'preset_3':
    BoardThumbnailButton(
        parent=preview_container,
        relative_width=0.25,
        relative_position=(0, 0.7),
        scale_mode='width',
        fen_string="sc3pcncpb3/5fc4/pa3pcncra3/pb1rd1Pd1Pb3/3pd1pb1Rd1Pd/3RaNaPa3Pc/4Fa5/3PdNaPa3Sa b",
        event=CustomEvent(ConfigEventType.PRESET_CLICK)
    ),
    'to_move_button':
    MultipleIconButton(
        parent=to_move_container,
        scale_mode='height',
        relative_position=(0, 0),
        relative_size=(1, 1),
        icons_dict=colour_icons,
        anchor_x='left',
        event=CustomEvent(ConfigEventType.COLOUR_CLICK)
    ),
    'to_move_text':
    Text(
        parent=to_move_container,
        relative_position=(0, 0),
        relative_size=(0.75, 1),
        fit_vertical=False,
        text='TO MOVE',
        anchor_x='right'
    ),
    'cpu_depth_carousel':
    Carousel(
        parent=config_container,
        relative_position=(0, 0.65),
        event=CustomEvent(ConfigEventType.CPU_DEPTH_CLICK),
        anchor_x='center',
        border_width=0,
        fill_colour=(0, 0, 0, 0),
        widgets_dict={
            2: Text(
                parent=config_container,
                relative_position=(0, 0),
                relative_size=(0.8, 0.075),
                text="EASY",
                margin=0,
                border_width=0,
                fill_colour=(0, 0, 0, 0)
            ),
            3: Text(
                parent=config_container,
                relative_position=(0, 0),
                relative_size=(0.8, 0.075),
                text="MEDIUM",
                margin=0,
                border_width=0,
                fill_colour=(0, 0, 0, 0)
            ),
            4: Text(
                parent=config_container,
                relative_position=(0, 0),
                relative_size=(0.8, 0.075),
                text="HARD",
                margin=0,
                border_width=0,
                fill_colour=(0, 0, 0, 0)
            ),
        }
    )
}