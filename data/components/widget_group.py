import pygame

class WidgetGroup(pygame.sprite.Group):
    def __init__(self, widget_list):
        super().__init__()
        for widget in widget_list:
            self.add(widget)
    
    def handle_resize(self, new_screen_size):
        for sprite in self.sprites():
            sprite.set_geometry(new_screen_size)
            sprite.set_image(new_screen_size)