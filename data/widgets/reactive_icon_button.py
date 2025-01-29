import pygame
from data.constants import WidgetState
from data.widgets.text import Text
from data.widgets.icon import Icon
from data.widgets.reactive_button import ReactiveButton
from data.managers.theme import theme

# ENLARGE_FACTOR = 1.2
# normal_text_size = kwargs.get('relative_size')
# enlarged_text_size = (normal_text_size[0] * ENLARGE_FACTOR, normal_text_size[1] * ENLARGE_FACTOR)

# base_text_colour = r, g, b = pygame.Color(kwargs.get('text_colour') or theme['textPrimary']).rgb
# hover_text_colour = (max(r - 35, 0), max(g - 35, 0), max(b - 35, 0))
# press_text_colour = (max(r - 75, 0), max(g - 75, 0), max(b - 75, 0))
#  if base_icon else        
#             Text(
#                 relative_position=(0, 0),
#                 relative_size=(0.4, 0.1),
#                 text=text,
#                 text_colour=base_text_colour,
#                 fill_colour=kwargs.get('fill_colour') or (0, 0, 0, 0),
#                 border_width=0,
#                 fit_vertical=True,
#                 center=text_center,
#             )

class ReactiveIconButton(ReactiveButton):
    def __init__(self, base_icon, hover_icon, press_icon, **kwargs):
        widgets_dict = {
            WidgetState.BASE: Icon(
                parent=kwargs.get('parent'),
                relative_size=kwargs.get('relative_size'),
                relative_position=(0, 0),
                icon=base_icon,
                fill_colour=(0, 0, 0, 0),
                border_width=0,
                margin=0,
                fit_icon=True,
            ),
            WidgetState.HOVER: Icon(
                parent=kwargs.get('parent'),
                relative_size=kwargs.get('relative_size'),
                relative_position=(0, 0),
                icon=hover_icon,
                fill_colour=(0, 0, 0, 0),
                border_width=0,
                margin=0,
                fit_icon=True,
            ),
            WidgetState.PRESS: Icon(
                parent=kwargs.get('parent'),
                relative_size=kwargs.get('relative_size'),
                relative_position=(0, 0),
                icon=press_icon,
                fill_colour=(0, 0, 0, 0),
                border_width=0,
                margin=0,
                fit_icon=True,
            )
        }

        super().__init__(
            widgets_dict=widgets_dict,
            **kwargs
        )