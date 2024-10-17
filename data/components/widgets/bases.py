import pygame
from data.constants import WidgetState

class _Widget(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        pass
    
    def set_image(self):
        raise NotImplementedError
    
    def set_geometry(self):
        raise NotImplementedError
    
    def set_screen_size(self, new_screen_size):
        raise NotImplementedError
    
    def process_event(self, event):
        raise NotImplementedError

class _Pressable:
    def __init__(self, down_func=None, up_func=None, hover_func=None, prolonged=False, **kwargs):
        self._down_func = down_func
        self._up_func = up_func
        self._hover_func = hover_func
        self._pressed = False
        self._prolonged = prolonged

        self._event = None

        self._widget_state = WidgetState.BASE

    def process_event(self, event):
        match event.type:
            case pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self._down_func()
                    self._widget_state = WidgetState.PRESS
            
            case pygame.MOUSEBUTTONUP:
                if self.rect.collidepoint(event.pos):
                    if self._widget_state == WidgetState.PRESS:
                        self._widget_state = WidgetState.BASE
                        self._up_func()
                        return self._event

                    elif self._widget_state == WidgetState.BASE:
                        self._hover_func()

                elif self._prolonged and self._widget_state == WidgetState.PRESS:
                    self._widget_state = WidgetState.BASE
                    self._up_func()
                    return self._event

            case pygame.MOUSEMOTION:
                if self.rect.collidepoint(event.pos):
                    if self._widget_state == WidgetState.PRESS:
                        return
                    elif self._widget_state == WidgetState.BASE:
                        self._hover_func()
                        self._widget_state = WidgetState.HOVER
                    elif self._widget_state == WidgetState.HOVER:
                        return
                else:
                    if self._prolonged is False:
                        self._up_func()
                        self._widget_state = WidgetState.BASE