from data.widgets import *
from data.components.custom_event import CustomEvent
from data.constants import ConfigEventType
from data.assets import GRAPHICS

def float_validator(num_string):
    try:
        float(num_string)
        return True
    except:
        return False

CONFIG_WIDGETS = {
    'default': [
        TextButton(
            relative_position=(0.5, 0.7),
            text='START NEW GAME',
            text_colour=(255, 0, 0),
            font_size=50,
            margin=20,
            minimum_width=400,
            event=CustomEvent(ConfigEventType.GAME_CLICK)
        ),
        TextInput(
            relative_position=(0.5, 0.1),
            placeholder='ENTER FEN STRING',
            size=(400, 75),
            border_width=5,
            margin=40,
            border_colour=(150, 150, 150),
            event_type=ConfigEventType.FEN_STRING_TYPE
        ),
        IconButton(
            relative_position=(0.5, 0.5),
            size=(180, 75),
            margin=10,
            border_width=5,
            border_radius=5,
            icon=GRAPHICS['pvp_button'],
            event=CustomEvent(ConfigEventType.PVP_CLICK)
        ),
        IconButton(
            relative_position=(0.92, 0.02),
            size=(50, 50),
            margin=10,
            border_width=5,
            border_radius=5,
            icon=GRAPHICS['home'],
            event=CustomEvent(ConfigEventType.MENU_CLICK)
        ),
        Carousel(
            relative_position=(0.1, 0.1),
            widgets_dict={
                0: Text(
                    relative_position=(0, 0),
                    text="hi",
                    font_size=30
                ),
                1: Text(
                    relative_position=(0, 0),
                    text="bye",
                ),
            }
        )
    ],
    'timer_text_input':
    TextInput(
        relative_position=(0.6, 0.3),
        placeholder='TIME CONTROL (MINS)',
        default='10',
        size=(300, 75),
        border_width=5,
        margin=50,
        validator=float_validator,
        border_colour=(150, 150, 150),
        event_type=ConfigEventType.TIME_TYPE
    ),
    'timer_button':
    IconButton(
        relative_position=(0.5, 0.3),
        size=(75, 75),
        margin=10,
        border_width=5,
        border_radius=5,
        icon=GRAPHICS['timer'],
        event=CustomEvent(ConfigEventType.TIME_CLICK)
    ),
    'pvc_button':
    MultipleIconButton(
        relative_position=(0.72, 0.5),
        size=(180, 75),
        margin=10,
        border_width=5,
        border_radius=5,
        icons_dict={0: GRAPHICS['pvc_button'], 1: GRAPHICS['home'], 2: GRAPHICS['pvp_button']},
        event=CustomEvent(ConfigEventType.PVC_CLICK)
    )
}