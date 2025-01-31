from data.widgets import *
from data.components.custom_event import CustomEvent
from data.constants import SettingsEventType, SHADER_MAP
from data.utils.data_helpers import get_user_settings
from data.assets import GRAPHICS
from data.managers.theme import theme

user_settings = get_user_settings()

carousel_widgets = {
    key: Text(
        relative_position=(0, 0),
        relative_size=(0.25, 0.04),
        margin=0,
        text=key.replace('_', ' ').upper(),
        fit_vertical=True,
        border_width=0,
        fill_colour=(0, 0, 0, 0),
    ) for key in SHADER_MAP.keys()
}

reset_container = Rectangle(
    relative_size=(0.2, 0.2),
    relative_position=(0, 0),
    fixed_position=(5, 5),
    anchor_x='right',
    anchor_y='bottom',
)

SETTINGS_WIDGETS = {
    'default': [
        reset_container,
        ReactiveIconButton(
            relative_position=(0, 0),
            relative_size=(0.075, 0.075),
            anchor_x='right',
            scale_mode='height',
            base_icon=GRAPHICS['home_base'],
            hover_icon=GRAPHICS['home_hover'],
            press_icon=GRAPHICS['home_press'],
            fixed_position=(5, 5),
            event=CustomEvent(SettingsEventType.MENU_CLICK)
        ),
        Text(
            relative_position=(0.01, 0.1),
            text='Display mode',
            relative_size=(0.4, 0.04),
            center=False,
            border_width=0,
            margin=0,
            fill_colour=(0, 0, 0, 0)
        ),
        Text(
            relative_position=(0.01, 0.2),
            text='Music',
            relative_size=(0.4, 0.04),
            center=False,
            border_width=0,
            margin=0,
            fill_colour=(0, 0, 0, 0)
        ),
        Text(
            relative_position=(0.01, 0.3),
            text='SFX',
            relative_size=(0.4, 0.04),
            center=False,
            border_width=0,
            margin=0,
            fill_colour=(0, 0, 0, 0)
        ),
        Text(
            relative_position=(0.01, 0.4),
            text='Primary board colour',
            relative_size=(0.4, 0.04),
            center=False,
            border_width=0,
            margin=0,
            fill_colour=(0, 0, 0, 0)
        ),
        Text(
            relative_position=(0.01, 0.5),
            text='Secondary board colour',
            relative_size=(0.4, 0.04),
            center=False,
            border_width=0,
            margin=0,
            fill_colour=(0, 0, 0, 0)
        ),
        Text(
            relative_position=(0.01, 0.6),
            text='Particles',
            relative_size=(0.4, 0.04),
            center=False,
            border_width=0,
            margin=0,
            fill_colour=(0, 0, 0, 0)
        ),
        Text(
            relative_position=(0.01, 0.7),
            text='Shaders (OPENGL GPU REQUIRED)',
            relative_size=(0.4, 0.04),
            center=False,
            border_width=0,
            margin=0,
            fill_colour=(0, 0, 0, 0)
        ),
        Text(
            relative_position=(0.01, 0.8),
            text='Super Secret Settings',
            relative_size=(0.4, 0.04),
            center=False,
            border_width=0,
            margin=0,
            fill_colour=(0, 0, 0, 0)
        ),
        TextButton(
            parent=reset_container,
            relative_position=(0, 0),
            relative_size=(1, 0.5),
            fit_vertical=False,
            margin=10,
            text='DISCARD CHANGES',
            text_colour=theme['textSecondary'],
            event=CustomEvent(SettingsEventType.RESET_USER)
        ),
        TextButton(
            parent=reset_container,
            relative_position=(0, 0.5),
            relative_size=(1, 0.5),
            fit_vertical=False,
            margin=10,
            text='RESET TO DEFAULT',
            text_colour=theme['textSecondary'],
            event=CustomEvent(SettingsEventType.RESET_DEFAULT)
        )
    ],
    'display_mode_dropdown':
    Dropdown(
        relative_position=(0.4, 0.1),
        relative_width=0.2,
        word_list=['fullscreen', 'windowed'],
        fill_colour=(255, 100, 100),
        event=CustomEvent(SettingsEventType.DROPDOWN_CLICK)
    ),
    'primary_colour_button':
    ColourButton(
        relative_position=(0.4, 0.4),
        relative_size=(0.08, 0.05),
        fill_colour=user_settings['primaryBoardColour'],
        border_width=5,
        event=CustomEvent(SettingsEventType.PRIMARY_COLOUR_BUTTON_CLICK)
    ),
    'secondary_colour_button':
    ColourButton(
        relative_position=(0.4, 0.5),
        relative_size=(0.08, 0.05),
        fill_colour=user_settings['secondaryBoardColour'],
        border_width=5,
        event=CustomEvent(SettingsEventType.SECONDARY_COLOUR_BUTTON_CLICK)
    ),
    'music_volume_slider':
    VolumeSlider(
        relative_position=(0.4, 0.2),
        relative_length=(0.5),
        default_volume=user_settings['musicVolume'],
        border_width=5,
        volume_type='music'
    ),
    'sfx_volume_slider':
    VolumeSlider(
        relative_position=(0.4, 0.3),
        relative_length=(0.5),
        default_volume=user_settings['sfxVolume'],
        border_width=5,
        volume_type='sfx'
    ),
    'shader_carousel':
    Carousel(
        relative_position = (0.4, 0.8),
        margin=5,
        border_width=0,
        fill_colour=(0, 0, 0, 0),
        widgets_dict=carousel_widgets,
        event=CustomEvent(SettingsEventType.SHADER_PICKER_CLICK),
    ),
    'particles_switch':
    Switch(
        relative_position=(0.4, 0.6),
        relative_height=0.04,
        event=CustomEvent(SettingsEventType.PARTICLES_CLICK)
    ),
    'opengl_switch':
    Switch(
        relative_position=(0.4, 0.7),
        relative_height=0.04,
        event=CustomEvent(SettingsEventType.OPENGL_CLICK)
    ),
}