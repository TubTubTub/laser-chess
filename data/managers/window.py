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

        self._screen_shake = None
        self._ctx = moderngl.create_context()
        self._shader_manager = ShaderManager(self._ctx, screen_size=self.size)

        if (selected_shader := get_user_settings()['shader']) is not None:
            for shader_type in SHADER_MAP[selected_shader]:
                self.set_effect(shader_type)

        # self._shader_manager.apply_shader(ShaderType.RAYS, lights=[
        #     [
        #         (0.5, 0.01),
        #         0.5,
        #         tuple(randint(0, 255) for _ in range(3))
        #     ],
        #     [
        #         (0.5, 0.5),
        #         0.5,
        #         tuple(randint(0, 255) for _ in range(3))
        #     ],
        #     [
        #         (0.01, 0.5),
        #         0.5,
        #         tuple(randint(0, 255) for _ in range(3))
        #     ],
        # ]) # POS BASED ON x and y, RADIUS BASED ON Y

        # self._shader_manager.apply_shader(ShaderType.BLOOM)
        
    def get_size(self):
        return self.size
    
    def reset_screen_shake(self):
        self._screen_shake = None
        self._position = (0, 0)
    
    def set_effect(self, effect, **kwargs):
        if effect == ShaderType.SHAKE:
            intensity = kwargs.get('intensity') or 10
            duration = kwargs.get('duration') or 500

            self._screen_shake = intensity
            animation.set_timer(duration, self.reset_screen_shake)
        
        elif isinstance(effect, ShaderType):
            self._shader_manager.apply_shader(effect, **kwargs)
    
    def clear_effects(self):
        self._shader_manager.clear_shaders()
    
    def draw(self):
        self._shader_manager.draw(self.get_surface())
        self.flip()
    
    def update(self):
        if self._screen_shake is not None:
            surface = self.get_surface()
            surface_copy = surface.copy()

            surface.fill((0, 0, 0, 0))
            surface.blit(surface_copy, (randint(0, self._screen_shake) - self._screen_shake / 2, randint(0, self._screen_shake) - self._screen_shake / 2))

        self.draw()
    
    def handle_resize(self):
        self._shader_manager.handle_resize(self.size)

is_fullscreen = get_user_settings()['displayMode'] == 'fullscreen'
window = WindowManager(size=SCREEN_SIZE, opengl=True, resizable=True, fullscreen=is_fullscreen)
screen = window.get_surface()
screen = screen.convert_alpha() SCREEN ALPHA NOT WORKING