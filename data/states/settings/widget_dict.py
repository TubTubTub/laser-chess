import pygame
from data.widgets import *
from data.components.custom_event import CustomEvent
from data.constants import SettingsEventType
from data.utils.data_helpers import get_user_settings
from data.assets import GRAPHICS

user_settings = get_user_settings()

if user_settings['displayMode'] == 'fullscreen':
    word_list = ['fullscreen', 'windowed']
else:
    word_list = ['windowed', 'fullscreen']

SETTINGS_WIDGETS = {
    'default': [
        Text(
            relative_position=(0.01, 0.2),
            text='Display mode',
            relative_size=(0.4, 0.04),
            center=False,
            border_width=0,
            margin=0,
            fill_colour=(0, 0, 0, 0)
        ),
        Text(
            relative_position=(0.01, 0.3),
            text='Music',
            relative_size=(0.4, 0.04),
            center=False,
            border_width=0,
            margin=0,
            fill_colour=(0, 0, 0, 0)
        ),
        Text(
            relative_position=(0.01, 0.4),
            text='SFX',
            relative_size=(0.4, 0.04),
            center=False,
            border_width=0,
            margin=0,
            fill_colour=(0, 0, 0, 0)
        ),
        Text(
            relative_position=(0.01, 0.5),
            text='Primary board colour',
            relative_size=(0.4, 0.04),
            center=False,
            border_width=0,
            margin=0,
            fill_colour=(0, 0, 0, 0)
        ),
        Text(
            relative_position=(0.01, 0.6),
            text='Secondary board colour',
            relative_size=(0.4, 0.04),
            center=False,
            border_width=0,
            margin=0,
            fill_colour=(0, 0, 0, 0)
        ),
        Text(
            relative_position=(0.01, 0.7),
            text='Animations (NOT IMPLEMENTED)',
            relative_size=(0.4, 0.04),
            center=False,
            border_width=0,
            margin=0,
            fill_colour=(0, 0, 0, 0)
        ),
        TextButton(
            relative_position=(0.01, 0.8),
            text='DISCARD CHANGES',
            text_colour=(255, 0, 0),
            margin=10,
            relative_size=(0.3, 0.1),
            event=CustomEvent(SettingsEventType.RESET_USER)
        ),
        TextButton(
            relative_position=(0.35, 0.8),
            text='RESET TO DEFAULT',
            text_colour=(255, 0, 0),
            margin=10,
            relative_size=(0.3, 0.1),
            event=CustomEvent(SettingsEventType.RESET_DEFAULT)
        ),
        Switch(
            relative_position=(0.4, 0.7),
            relative_height=0.04,
            fill_colour=(0, 0, 255),
            event=None
        ),
        IconButton(
            relative_position=(0.9, 0.05),
            relative_size=(0.07, 0.1),
            margin=10,
            icon=GRAPHICS['home'],
            event=CustomEvent(SettingsEventType.MENU_CLICK)
        )
    ],
    'display_mode_dropdown':
    Dropdown(
        relative_position=(0.4, 0.2),
        relative_size=(0.2, 0.2),
        word_list=word_list,
        fill_colour=(255, 100, 100),
        event=CustomEvent(SettingsEventType.DROPDOWN_CLICK)
    ),
    'primary_colour_button':
    ColourButton(
        relative_position=(0.4, 0.5),
        relative_size=(0.08, 0.05),
        default_colour=pygame.Color(user_settings['primaryBoardColour']).rgb,
        border_width=5,
        event=CustomEvent(SettingsEventType.PRIMARY_COLOUR_BUTTON_CLICK)
    ),
    'secondary_colour_button':
    ColourButton(
        relative_position=(0.4, 0.6),
        relative_size=(0.08, 0.05),
        default_colour=pygame.Color(user_settings['secondaryBoardColour']).rgb,
        border_width=5,
        event=CustomEvent(SettingsEventType.SECONDARY_COLOUR_BUTTON_CLICK)
    ),
    'music_volume_slider':
    VolumeSlider(
        relative_position=(0.4, 0.3),
        relative_length=(0.5),
        default_volume=user_settings['musicVolume'],
        border_width=5,
        volume_type='music'
    ),
    'sfx_volume_slider':
    VolumeSlider(
        relative_position=(0.4, 0.4),
        relative_length=(0.5),
        default_volume=user_settings['sfxVolume'],
        border_width=5,
        volume_type='sfx'
    )
}