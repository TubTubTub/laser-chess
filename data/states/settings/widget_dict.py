from data.widgets import *
from data.components.custom_event import CustomEvent
from data.constants import SettingsEventType, SHADER_MAP
from data.utils.data_helpers import get_user_settings
from data.assets import GRAPHICS

user_settings = get_user_settings()

carousel_widgets = {
    key: Text(
        relative_position=(0, 0),
        relative_size=(0.2, 0.04),
        margin=0,
        text=key.replace('_', ' ').upper(),
        fit_vertical=True,
        border_width=0,
        fill_colour=(0, 0, 0, 0),
    ) for key in SHADER_MAP.keys()
}

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
            text='Particles',
            relative_size=(0.4, 0.04),
            center=False,
            border_width=0,
            margin=0,
            fill_colour=(0, 0, 0, 0)
        ),
        Text(
            relative_position=(0.01, 0.8),
            text='Shaders (OPENGL GPU REQUIRED)',
            relative_size=(0.4, 0.04),
            center=False,
            border_width=0,
            margin=0,
            fill_colour=(0, 0, 0, 0)
        ),
        Text(
            relative_position=(0.01, 0.9),
            text='Super Secret Settings',
            relative_size=(0.4, 0.04),
            center=False,
            border_width=0,
            margin=0,
            fill_colour=(0, 0, 0, 0)
        ),
        TextButton(
            relative_position=(0.3, 0.2),
            relative_size=(0.3, 0.1),
            text='DISCARD CHANGES',
            anchor_x='right',
            anchor_y='bottom',
            text_colour=(255, 0, 0),
            margin=10,
            event=CustomEvent(SettingsEventType.RESET_USER)
        ),
        TextButton(
            relative_position=(0.3, 0.1),
            relative_size=(0.3, 0.1),
            text='RESET TO DEFAULT',
            anchor_x='right',
            anchor_y='bottom',
            text_colour=(255, 0, 0),
            margin=10,
            event=CustomEvent(SettingsEventType.RESET_DEFAULT)
        ),
        IconButton(
            relative_position=(0.1, 0.05),
            relative_size=(0.1, 0.1),
            scale_mode='height',
            margin=10,
            icon=GRAPHICS['home'],
            anchor_x='right',
            fixed_position=True,
            event=CustomEvent(SettingsEventType.MENU_CLICK)
        )
    ],
    'display_mode_dropdown':
    Dropdown(
        relative_position=(0.4, 0.2),
        relative_width=0.2,
        word_list=['fullscreen', 'windowed'],
        fill_colour=(255, 100, 100),
        event=CustomEvent(SettingsEventType.DROPDOWN_CLICK)
    ),
    'primary_colour_button':
    ColourButton(
        relative_position=(0.4, 0.5),
        relative_size=(0.08, 0.05),
        fill_colour=user_settings['primaryBoardColour'],
        border_width=5,
        event=CustomEvent(SettingsEventType.PRIMARY_COLOUR_BUTTON_CLICK)
    ),
    'secondary_colour_button':
    ColourButton(
        relative_position=(0.4, 0.6),
        relative_size=(0.08, 0.05),
        fill_colour=user_settings['secondaryBoardColour'],
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
    ),
    'shader_carousel':
    Carousel(
        relative_position = (0.4, 0.9),
        margin=5,
        border_width=0,
        fill_colour=(0, 0, 0, 0),
        widgets_dict=carousel_widgets,
        event=CustomEvent(SettingsEventType.SHADER_PICKER_CLICK),
    ),
    'particles_switch':
    Switch(
        relative_position=(0.4, 0.7),
        relative_height=0.04,
        fill_colour=(0, 0, 255),
        event=CustomEvent(SettingsEventType.PARTICLES_CLICK)
    ),
    'opengl_switch':
    Switch(
        relative_position=(0.4, 0.8),
        relative_height=0.04,
        fill_colour=(0, 0, 255),
        event=CustomEvent(SettingsEventType.OPENGL_CLICK)
    ),
}