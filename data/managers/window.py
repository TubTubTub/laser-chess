import pygame
import moderngl
from random import randint
from data.utils.data_helpers import get_user_settings
from data.constants import ShaderType, SCREEN_SIZE
from data.managers.animation import animation
from data.managers.shader import ShaderManager

class WindowManager(pygame.Window):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.get_surface() # Initialise convert format

        self._screen_shake = None
        self._ctx = moderngl.create_context()
        self._shader_manager = ShaderManager(self._ctx, screen_size=self.size)
        self._shader_manager.apply_shader(ShaderType.RAYS, light_positions=[(0.5, 0.5), (0.5, 0.1), (0.5, 0.5), (0.5, 0.1)], light_radii=[500, 200, 500, 200]) # DON'T PUT LIGHT ON EDGE
    
    def get_size(self):
        return self.size
    
    def reset_screen_shake(self):
        self._screen_shake = None
        self._position = (0, 0)
    
    def set_effect(self, effect, **kwargs):
        match effect:
            case ShaderType.SHAKE:
                intensity = kwargs.get('intensity') or 10
                duration = kwargs.get('duration') or 500

                self._screen_shake = intensity
                animation.set_timer(duration, self.reset_screen_shake)
    
    def draw(self):
        self._shader_manager.draw(self.get_surface())
        self.flip()
    
    def update(self):
        if self._screen_shake is not None:
            surface = self.get_surface()
            surface_copy = surface.copy()

            surface.fill((0, 0, 0))
            surface.blit(surface_copy, (randint(0, self._screen_shake) - self._screen_shake / 2, randint(0, self._screen_shake) - self._screen_shake / 2))

        self.draw()
    
    def handle_resize(self):
        self._shader_manager.handle_resize(self.size)

is_fullscreen = get_user_settings()['displayMode'] == 'fullscreen'
window = WindowManager(size=SCREEN_SIZE, opengl=True, resizable=True, fullscreen=is_fullscreen)
screen = window.get_surface()