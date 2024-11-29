import pygame
from data.constants import WidgetState
from data.components.audio import audio
from data.assets import SFX

screen = pygame.display.get_surface()

class _Widget(pygame.sprite.Sprite):
    def __init__(self, surface=screen):
        super().__init__()
        self._surface = surface
        self._surface_size = surface.get_size()
    
    def set_image(self):
        raise NotImplementedError
    
    def set_geometry(self):
        raise NotImplementedError
    
    def set_surface_size(self, new_surface_size):
        raise NotImplementedError
    
    def process_event(self, event):
        raise NotImplementedError

class _Pressable:
    def __init__(self, event, down_func=None, up_func=None, hover_func=None, prolonged=False, play_sfx=True, **kwargs):
        self._down_func = down_func
        self._up_func = up_func
        self._hover_func = hover_func
        self._pressed = False
        self._prolonged = prolonged
        self._play_sfx = play_sfx
        self._sfx = SFX['button_click']

        self._event = event

        self._widget_state = WidgetState.BASE
    
    def get_widget_state(self):
        return self._widget_state

    def process_event(self, event):
        match event.type:
            case pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self._down_func()
                    self._widget_state = WidgetState.PRESS
            
            case pygame.MOUSEBUTTONUP:
                if self.rect.collidepoint(event.pos):
                    if self._widget_state == WidgetState.PRESS:
                        if self._play_sfx:
                            audio.play_sfx(self._sfx)

                        self._up_func()
                        self._widget_state = WidgetState.HOVER
                        return self._event

                    elif self._widget_state == WidgetState.BASE:
                        self._hover_func()

                elif self._prolonged and self._widget_state == WidgetState.PRESS:
                    if self._play_sfx:
                        audio.play_sfx(self._sfx)
                    self._up_func()
                    self._widget_state = WidgetState.BASE
                    return self._event

            case pygame.MOUSEMOTION:
                if self.rect.collidepoint(event.pos):
                    if self._widget_state == WidgetState.PRESS:
                        return
                    elif self._widget_state == WidgetState.BASE:
                        self._hover_func()
                        self._widget_state = WidgetState.HOVER
                    elif self._widget_state == WidgetState.HOVER:
                        self._hover_func()
                else:
                    if self._prolonged is False:
                        if self._widget_state in [WidgetState.PRESS, WidgetState.HOVER]:
                            self._widget_state = WidgetState.BASE
                            self._up_func()
                        elif self._widget_state == WidgetState.BASE:
                            return
                    elif self._prolonged is True:
                        if self._widget_state in [WidgetState.PRESS, WidgetState.BASE]:
                            return
                        else:
                            self._widget_state = WidgetState.BASE
                            self._up_func()