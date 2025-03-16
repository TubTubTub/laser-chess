from data.components.custom_event import CustomEvent
from data.utils.event_types import MenuEventType
from data.utils.assets import GRAPHICS
from data.managers.theme import theme
from data.widgets import *

top_right_container = Rectangle(
    relative_position=(0, 0),
    relative_size=(0.15, 0.075),
    fixed_position=(5, 5),
    anchor_x='right',
    scale_mode='height'
)

MENU_WIDGETS = {
    'credits':
    Icon(
        relative_position=(0, 0),
        relative_size=(0.7, 0.7),
        icon=GRAPHICS['credits'],
        anchor_x='center',
        anchor_y='center',
        margin=50
    ),
    'default': [
        top_right_container,
        Rectangle(
            relative_position=(0.65, 0.15),
            relative_size=(0.15, 0.15),
            scale_mode='height',
            border_width=0,
            border_radius=50,
            fill_colour=theme['fillSecondary'],
            visible=True
        ),
        Rectangle(
            relative_position=(0.8, 0.1),
            relative_size=(0.10, 0.10),
            scale_mode='height',
            border_width=0,
            border_radius=100,
            fill_colour=theme['fillSecondary'],
            visible=True
        ),
        Rectangle(
            relative_position=(0.5, 0.1),
            relative_size=(0.20, 0.20),
            scale_mode='height',
            border_width=0,
            border_radius=10,
            fill_colour=theme['fillSecondary'],
            visible=True
        ),
        Rectangle(
            relative_position=(0.9, 0.2),
            relative_size=(0.15, 0.15),
            scale_mode='height',
            border_width=0,
            border_radius=20,
            fill_colour=theme['fillSecondary'],
            visible=True
        ),
        Rectangle(
            relative_position=(0.85, 0.4),
            relative_size=(0.20, 0.20),
            scale_mode='height',
            border_width=0,
            border_radius=30,
            fill_colour=theme['fillSecondary'],
            visible=True
        ),
        Rectangle(
            relative_position=(0.7, 0.4),
            relative_size=(0.10, 0.10),
            scale_mode='height',
            border_width=0,
            border_radius=50,
            fill_colour=theme['fillSecondary'],
            visible=True
        ),
        ReactiveIconButton(
            parent=top_right_container,
            relative_position=(0, 0),
            relative_size=(1, 1),
            anchor_x='right',
            scale_mode='height',
            base_icon=GRAPHICS['quit_base'],
            hover_icon=GRAPHICS['quit_hover'],
            press_icon=GRAPHICS['quit_press'],
            event=CustomEvent(MenuEventType.QUIT_CLICK)
        ),
        ReactiveIconButton(
            parent=top_right_container,
            relative_position=(0, 0),
            relative_size=(1, 1),
            scale_mode='height',
            base_icon=GRAPHICS['credits_base'],
            hover_icon=GRAPHICS['credits_hover'],
            press_icon=GRAPHICS['credits_press'],
            event=CustomEvent(MenuEventType.CREDITS_CLICK)
        ),
        ReactiveIconButton(
            relative_position=(0.05, -0.2),
            relative_size=(0, 0.15),
            anchor_y='center',
            base_icon=GRAPHICS['play_text_base'],
            hover_icon=GRAPHICS['play_text_hover'],
            press_icon=GRAPHICS['play_text_press'],
            event=CustomEvent(MenuEventType.CONFIG_CLICK)
        ),
        ReactiveIconButton(
            relative_position=(0.05, 0),
            relative_size=(0, 0.15),
            anchor_y='center',
            base_icon=GRAPHICS['review_text_base'],
            hover_icon=GRAPHICS['review_text_hover'],
            press_icon=GRAPHICS['review_text_press'],
            event=CustomEvent(MenuEventType.BROWSER_CLICK)
        ),
        ReactiveIconButton(
            relative_position=(0.05, 0.2),
            relative_size=(0, 0.15),
            anchor_y='center',
            base_icon=GRAPHICS['settings_text_base'],
            hover_icon=GRAPHICS['settings_text_hover'],
            press_icon=GRAPHICS['settings_text_press'],
            event=CustomEvent(MenuEventType.SETTINGS_CLICK)
        ),
        # Icon(
        #     relative_position=(0.0, 0.1),
        #     relative_size=(0.3, 0.2),
        #     anchor_x='center',
        #     fill_colour=theme['fillSecondary'],
        #     icon=GRAPHICS['title_screen_art'],
        #     stretch=False
        # ),
    ]
}

# Widgets used for testing light rays effect
TEST_WIDGETS = {
    'default': [
        Rectangle(
            relative_position=(0.4, 0.2),
            relative_size=(0.1, 0.1),
            scale_mode='height',
            visible=True,
            border_width=0,
            fill_colour=(255, 0, 0),
            border_radius=1000
        ),
        Rectangle(
            relative_position=(0.5, 0.7),
            relative_size=(0.1, 0.1),
            scale_mode='height',
            visible=True,
            border_width=0,
            fill_colour=(255, 0, 0),
            border_radius=1000
        ),
        Rectangle(
            relative_position=(0.6, 0.6),
            relative_size=(0.2, 0.2),
            scale_mode='height',
            visible=True,
            border_width=0,
            fill_colour=(255, 0, 0),
            border_radius=1000
        ),
        Rectangle(
            relative_position=(0.4, 0.6),
            relative_size=(0.1, 0.1),
            scale_mode='height',
            visible=True,
            border_width=0,
            fill_colour=(255, 0, 0),
            border_radius=1000
        ),
        Rectangle(
            relative_position=(0.6, 0.4),
            relative_size=(0.1, 0.1),
            scale_mode='height',
            visible=True,
            border_width=0,
            fill_colour=(255, 0, 0),
            border_radius=1000
        ),
        Rectangle(
            relative_position=(0.3, 0.4),
            relative_size=(0.1, 0.1),
            scale_mode='height',
            visible=True,
            border_width=0,
            fill_colour=(255, 0, 0),
            border_radius=1000
        ),
        Rectangle(
            relative_position=(0.475, 0.15),
            relative_size=(0.2, 0.2),
            scale_mode='height',
            visible=True,
            border_width=0,
            fill_colour=(255, 0, 0),
            border_radius=1000
        ),
        Rectangle(
            relative_position=(0.6, 0.2),
            relative_size=(0.1, 0.1),
            scale_mode='height',
            visible=True,
            border_width=0,
            fill_colour=(255, 0, 0),
            border_radius=1000
        )
    ]
}