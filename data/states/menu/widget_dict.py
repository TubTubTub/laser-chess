from data.widgets import *
from data.components.custom_event import CustomEvent
from data.constants import MenuEventType, WidgetState
from data.assets import GRAPHICS

from data.managers.theme import theme

MENU_WIDGETS = {
    'default': [
        ReactiveIconButton(
            relative_position=(0.05, -0.2),
            relative_size=(0, 0.15),
            anchor_y='center',
            base_icon=GRAPHICS['play_base'],
            hover_icon=GRAPHICS['play_hover'],
            press_icon=GRAPHICS['play_press'],
            fit_icon=True,
            fill_colour=(0, 0, 0, 0),
            event=CustomEvent(MenuEventType.CONFIG_CLICK)
        ),
        ReactiveIconButton(
            relative_position=(0.05, 0),
            relative_size=(0, 0.15),
            anchor_y='center',
            base_icon=GRAPHICS['review_base'],
            hover_icon=GRAPHICS['review_hover'],
            press_icon=GRAPHICS['review_press'],
            fit_icon=True,
            fill_colour=(0, 0, 0, 0),
            event=CustomEvent(MenuEventType.BROWSER_CLICK)
        ),
        ReactiveIconButton(
            relative_position=(0.05, 0.2),
            relative_size=(0, 0.15),
            anchor_y='center',
            base_icon=GRAPHICS['settings_base'],
            hover_icon=GRAPHICS['settings_hover'],
            press_icon=GRAPHICS['settings_press'],
            fit_icon=True,
            fill_colour=(0, 0, 0, 0),
            event=CustomEvent(MenuEventType.SETTINGS_CLICK)
        ),
        Icon(
            relative_position=(0.0, 0.1),
            relative_size=(0.3, 0.2),
            anchor_x='center',
            fill_colour=theme['fillSecondary'],
            icon=GRAPHICS['title_screen_art'],
            stretch=False
        ),
    ]
}