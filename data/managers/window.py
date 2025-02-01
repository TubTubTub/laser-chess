import pygame
import moderngl
from random import randint
from data.utils.data_helpers import get_user_settings
from data.constants import ShaderType, SCREEN_SIZE, SHADER_MAP
from data.managers.animation import animation
from data.managers.shader import ShaderManager


class WindowManager(pygame.Window):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.get_surface() # Initialise convert format
        
        self._ctx = moderngl.create_context()
        self._shader_manager = ShaderManager(self._ctx, screen_size=self.size)
        self.screen = pygame.Surface(self.size, pygame.SRCALPHA)

        self.shader_arguments = {
            ShaderType.BASE: {},
            ShaderType.SHAKE: {},
            ShaderType.BLOOM: {},
            ShaderType.GRAYSCALE: {},
            ShaderType.CRT: {},
            ShaderType.RAYS: {}
        }

        if (selected_shader := get_user_settings()['shader']) is not None:
            for shader_type in SHADER_MAP[selected_shader]:
                self.set_effect(shader_type)
    
    def set_effect(self, effect, **kwargs):
        self._shader_manager.apply_shader(effect, **kwargs)
    
    def set_apply_arguments(self, effect, **kwargs):
        self.shader_arguments[effect] = kwargs
    
    def clear_apply_arguments(self, effect):
        self.shader_arguments[effect] = {}
    
    def clear_effect(self, effect):
        self._shader_manager.remove_shader(effect)
        self.clear_apply_arguments(effect)
    
    def clear_all_effects(self):
        self._shader_manager.clear_shaders()

        for shader_type in self.shader_arguments:
            self.shader_arguments[shader_type] = {}
    
    def draw(self):
        # native_surface = self.get_surface()
        # native_surface.fill((0, 0, 0))
        # native_surface.blit(self.screen, (0, 0))
        self._shader_manager.draw(self.screen, self.shader_arguments)
        self.flip()
    
    def update(self):
        self.draw()
    
    def handle_resize(self):
        self._shader_manager.handle_resize(self.size)
        self.screen = pygame.Surface(self.size, pygame.SRCALPHA)

is_fullscreen = get_user_settings()['displayMode'] == 'fullscreen'
window = WindowManager(size=SCREEN_SIZE, opengl=True, resizable=True, fullscreen=is_fullscreen)