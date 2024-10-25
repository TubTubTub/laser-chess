import pygame
from data.components.widgets import *
from data.components.custom_event import CustomEvent
from data.constants import SettingsEventType
from data.utils.settings_helpers import get_user_settings
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
            font_size=30,
            text_colour=(255, 255, 255),
            margin=0,
            fill_colour=(0, 0, 0, 0)
        ),
        Text(
            relative_position=(0.01, 0.3),
            text='Music',
            font_size=30,
            text_colour=(255, 255, 255),
            margin=0,
            fill_colour=(0, 0, 0, 0)
        ),
        Text(
            relative_position=(0.01, 0.4),
            text='SFX',
            font_size=30,
            text_colour=(255, 255, 255),
            margin=0,
            fill_colour=(0, 0, 0, 0)
        ),
        Text(
            relative_position=(0.01, 0.5),
            text='Primary board colour',
            font_size=30,
            text_colour=(255, 255, 255),
            margin=0,
            fill_colour=(0, 0, 0, 0)
        ),
        Text(
            relative_position=(0.01, 0.6),
            text='Secondary board colour',
            font_size=30,
            text_colour=(255, 255, 255),
            margin=0,
            fill_colour=(0, 0, 0, 0)
        ),
        Text(
            relative_position=(0.01, 0.7),
            text='Animations (NOT IMPLEMENTED)',
            font_size=30,
            text_colour=(255, 255, 255),
            margin=0,
            fill_colour=(0, 0, 0, 0)
        ),
        TextButton(
            relative_position=(0.01, 0.85),
            text='DISCARD CHANGES',
            text_colour=(255, 0, 0),
            margin=20,
            font_size=30,
            event=CustomEvent(SettingsEventType.RESET_USER)
        ),
        TextButton(
            relative_position=(0.25, 0.85),
            text='RESET TO DEFAULT',
            text_colour=(255, 0, 0),
            margin=20,
            font_size=30,
            event=CustomEvent(SettingsEventType.RESET_DEFAULT)
        ),
        Switch(
            relative_position=(0.35, 0.7),
            relative_length=(0.1),
            colour=(0, 0, 255),
            event=None
        ),
        IconButton(
            relative_position=(0.9, 0.1),
            size=(50, 50),
            margin=10,
            border_width=5,
            border_radius=5,
            icon=GRAPHICS['home'],
            event=CustomEvent(SettingsEventType.MENU_CLICK)
        )
    ],
    'display_mode_dropdown':
    Dropdown(
        relative_position=(0.35, 0.175),
        word_list=word_list,
        font_size=25,
        fill_colour=(255, 100, 100),
        event=CustomEvent(SettingsEventType.DROPDOWN_CLICK)
    ),
    'primary_colour_button':
    ColourButton(
        relative_position=(0.35, 0.5),
        relative_size=(0.1, 0.05),
        default_colour=pygame.Color(user_settings['primaryBoardColour']).rgb,
        border_width=5,
        event=CustomEvent(SettingsEventType.COLOUR_BUTTON_CLICK, colour_type='primary')
    ),
    'secondary_colour_button':
    ColourButton(
        relative_position=(0.35, 0.6),
        relative_size=(0.1, 0.05),
        default_colour=pygame.Color(user_settings['secondaryBoardColour']).rgb,
        border_width=5,
        event=CustomEvent(SettingsEventType.COLOUR_BUTTON_CLICK, colour_type='secondary')
    ),
    'music_volume_slider':
    VolumeSlider(
        relative_position=(0.35, 0.274),
        relative_length=(0.5),
        default_volume=user_settings['musicVolume'],
        border_width=5,
        volume_type='music'
    ),
    'sfx_volume_slider':
    VolumeSlider(
        relative_position=(0.35, 0.376),
        relative_length=(0.5),
        default_volume=user_settings['sfxVolume'],
        border_width=5,
        volume_type='sfx'
    )
}