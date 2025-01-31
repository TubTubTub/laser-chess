import pygame
from data.managers.window import window

class WidgetGroup(pygame.sprite.Group):
    def __init__(self, widget_dict):
        super().__init__()

        for value in widget_dict.values():
            if isinstance(value, list):
                for widget in value:
                    self.add(widget)
            elif isinstance(value, dict):
                for widget in value.values():
                    self.add(widget)
            else:
                self.add(value)
    
    def handle_resize(self, new_surface_size):
        for sprite in self.sprites():
            sprite.set_surface_size(new_surface_size)
            sprite.set_image()
            sprite.set_geometry()
    
    def process_event(self, event):
        for sprite in self.sprites():
            widget_event = sprite.process_event(event)

            if widget_event:
                return widget_event
        
        return None
    
    def draw(self):
        sprites = self.sprites()
        for spr in sprites:
            surface = spr._surface or window.screen
            self.spritedict[spr] = surface.blit(spr.image, spr.rect)
        self.lostsprites = []
        dirty = self.lostsprites

        return dirty
    
    def on_widget(self, mouse_pos):
        test_sprite = pygame.sprite.Sprite()
        test_sprite.rect = pygame.FRect(*mouse_pos, 1, 1)
        return pygame.sprite.spritecollideany(test_sprite, self)