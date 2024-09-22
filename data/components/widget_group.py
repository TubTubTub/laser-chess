import pygame
from data.components.widgets import Text
from data.components.game_event import GameEvent
from data.constants import EventType, RotationDirection

class WidgetGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
    
    def initialise_widgets(self, screen_size):
        clockwise_button = Text(
            event=GameEvent.create_event(EventType.ROTATE_PIECE, rotation_direction=RotationDirection.CLOCKWISE),
            screen_size=screen_size,position=(200, 200),
            text='CLOCKWISE',
            text_colour=(255, 0, 0)
        )
        self.add(clockwise_button)
    
    def handle_resize(self, new_screen_size):
        for sprite in self.sprites():
            sprite.set_geometry(new_screen_size)
            sprite.set_image(new_screen_size)