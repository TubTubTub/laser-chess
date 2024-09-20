import pygame
from data.components.widgets import Text

class WidgetGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
    
    def initialise_widgets(self, screen_size):
        text1 = Text(screen_size=screen_size, position=(200, 200), text='Hi', text_colour=(255, 0, 0))
        self.add(text1)
    
    def handle_resize(self, new_screen_size):
        for sprite in self.sprites():
            sprite.set_geometry(new_screen_size)
            sprite.set_image(new_screen_size)