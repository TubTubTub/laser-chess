import pygame

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
    def __init__(self, down_func=None, up_func=None, hover_func=None, **kwargs):
        self._down_func = down_func
        self._up_func = up_func
        self._hover_func = hover_func
        self._pressed = False

    def process_event(self, event):
        match event.type:
            case pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self._down_func()
                    self._pressed = True
            
            case pygame.MOUSEBUTTONUP:
                if self.rect.collidepoint(event.pos):
                    self._hover_func()
                    
                    if self._pressed:
                        self._pressed = False
                        return self._event
            
            case pygame.MOUSEMOTION:
                if self.rect.collidepoint(event.pos):
                    if self._pressed:
                        self._down_func()
                    else:
                        self._hover_func()
                else:
                    self._up_func()
                    self._pressed = False