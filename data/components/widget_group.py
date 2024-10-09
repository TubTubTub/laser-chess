import pygame

class WidgetGroup(pygame.sprite.Group):
    def __init__(self, widget_list):
        super().__init__()
        for widget in widget_list:
            self.add(widget)
    
    def handle_resize(self, new_screen_size):
        for sprite in self.sprites():
            sprite.set_screen_size(new_screen_size)
            sprite.set_image()
            sprite.set_geometry()
    
    def process_event(self, event):
        for sprite in self.sprites():
            widget_event = sprite.process_event(event)

            if widget_event:
                return widget_event
        
        return None