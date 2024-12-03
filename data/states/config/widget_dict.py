import pygame
from data.widgets import *
from data.states.config.default_config import default_config
from data.components.custom_event import CustomEvent
from data.constants import ConfigEventType
from data.assets import GRAPHICS
from data.utils.asset_helpers import get_dimmed_icon

from copy import deepcopy

screen = pygame.display.get_surface()

def float_validator(num_string):
    try:
        float(num_string)
        return True
    except:
        return False

if default_config['CPU_ENABLED']:
    pvp_icons = {False: GRAPHICS['pvp_button'], True: GRAPHICS['pvp_button']}
    pvc_icons = {True: GRAPHICS['pvc_button'], False: GRAPHICS['pvc_button']}
    pvc_locked = True
    pvp_locked = False
else:
    pvp_icons = {True: GRAPHICS['pvp_button'], False: GRAPHICS['pvp_button']}
    pvc_icons = {False: GRAPHICS['pvc_button'], True: GRAPHICS['pvc_button']}
    pvc_locked = False
    pvp_locked = True

if default_config['TIME_ENABLED']:
    time_enabled_icons = {True: GRAPHICS['timer'], False: get_dimmed_icon(GRAPHICS['timer'])}
else:
    time_enabled_icons = {False: get_dimmed_icon(GRAPHICS['timer']), True: GRAPHICS['timer']}

config_container = Rectangle(
    relative_position=(0.5, 0.1),
    relative_size=(0.4, 0.8)
)

CONFIG_WIDGETS = {
    'default': [
        TextInput(
            surface=config_container,
            relative_position=(0.1, 0.1),
            placeholder='ENTER FEN STRING',
            default='sc3ncfancpb2/2pc7/3Pd7/pa1Pc1rbra1pb1Pd/pb1Pd1RaRb1pa1Pc/6pb3/7Pa2/2PdNaFaNa3Sa b',
            relative_size=(0.8, 0.2),
            border_width=5,
            margin=0,
            border_colour=(150, 150, 150),
            event_type=ConfigEventType.FEN_STRING_TYPE
        ),
        TextInput(
            surface=config_container,
            relative_position=(0.6, 0.3),
            placeholder='TIME CONTROL (MINS)',
            default=str(default_config['TIME']),
            relative_size=(0.3, 0.1),
            border_width=5,
            margin=0,
            validator=float_validator,
            border_colour=(150, 150, 150),
            event_type=ConfigEventType.TIME_TYPE
        ),
        Text(
            surface=config_container,
            relative_size=(0.3, 0.3),
            relative_position=(0.82, 0.31),
            text='MINS',
            margin=30
        ),
        IconButton(
            surface=config_container,
            relative_position=(0.92, 0.02),
            relative_size=(0.3, 0.3),
            margin=10,
            border_width=5,
            border_radius=5,
            icon=GRAPHICS['home'],
            event=CustomEvent(ConfigEventType.MENU_CLICK)
        ),
        config_container,
    ],
    'start_button':
    TextButton(
        relative_position=(0.5, 0.7),
        relative_size=(0.3, 0.3),
        text='START NEW GAME',
        text_colour=(255, 0, 0),
        font_size=50,
        margin=20,
        minimum_width=400,
        event=CustomEvent(ConfigEventType.GAME_CLICK)
    ),
    'timer_button':
    MultipleIconButton(
        relative_position=(0.5, 0.3),
        relative_size=(0.3, 0.3),
        margin=0,
        border_width=5,
        border_radius=5,
        icons_dict=time_enabled_icons,
        event=CustomEvent(ConfigEventType.TIME_CLICK)
    ),
    'pvp_button':
    MultipleIconButton(
        relative_position=(0.5, 0.5),
        relative_size=(0.3, 0.3),
        margin=0,
        border_width=5,
        border_radius=5,
        icons_dict=pvp_icons,
        locked=pvp_locked,
        stretch=False,
        event=CustomEvent(ConfigEventType.PVP_CLICK)
    ),
    'pvc_button':
    MultipleIconButton(
        relative_position=(0.72, 0.5),
        relative_size=(0.3, 0.3),
        margin=0,
        border_width=5,
        border_radius=5,
        icons_dict=pvc_icons,
        locked=pvc_locked,
        stretch=False,
        event=CustomEvent(ConfigEventType.PVC_CLICK)
    ),
    'invalid_fen_string':
    Text(
        relative_position=(0.5, 0.24),
        relative_size=(0.3, 0.3),
        minimum_width=400,
        text='INVALID FEN STRING!',
        margin=10,
        fill_colour=(100, 0, 0),
        text_colour=(255, 0, 0),
    ),
    'board_thumbnail':
    BoardThumbnail(
        surface=screen,
        relative_position=(0.02, 0.15),
        relative_width=0.5
    )
}