import pygame
from data.constants import ScreenEffect
from data.components.animation import animation
from random import randint

class ScreenManager(pygame.Surface):
    def __init__(self):
        self._pygame_screen = pygame.display.get_surface()
        self._position = (0, 0)

        self._screen_shake = None

        super().__init__(self._pygame_screen.size)
    
    def resize_surface(self):
        self = pygame.transform.scale(self, self._pygame_screen.size)
    
    def reset_screen_shake(self):
        self._screen_shake = None
        self._position = (0, 0)
    
    def set_effect(self, effect, **kwargs):
        match effect:
            case ScreenEffect.SHAKE:
                intensity = kwargs.get('intensity') or 10
                duration = kwargs.get('duration') or 500

                self._screen_shake = intensity
                animation.set_timer(duration, self.reset_screen_shake)
    
    def update(self):
        if self._screen_shake is not None:
            self._position = (randint(0, self._screen_shake) - self._screen_shake / 2, randint(0, self._screen_shake) - self._screen_shake / 2)

        self.draw()
    
    def draw(self):
        self._pygame_screen.blit(self, self._position)

screen = ScreenManager()