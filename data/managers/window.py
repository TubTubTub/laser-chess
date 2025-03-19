import pygame
import moderngl
from data.utils.constants import ShaderType, SCREEN_SIZE, SHADER_MAP
from data.helpers.data_helpers import get_user_settings
from data.helpers.asset_helpers import draw_background
from data.managers.shader import ShaderManager

user_settings = get_user_settings()
is_opengl = user_settings['opengl']
is_fullscreen = user_settings['displayMode'] == 'fullscreen'

class WindowManager(pygame.Window):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._native_screen = self.get_surface() # Initialise convert format
        self.screen = pygame.Surface(self.size, pygame.SRCALPHA)

        if is_opengl:
            self._ctx = moderngl.create_context()
            self._shader_manager = ShaderManager(self._ctx, screen_size=self.size)

            # Each ShaderType contains a dictionary of kwargs, used as arguments when running the apply method on the corresponding shader class
            self.shader_arguments = {
                ShaderType.BASE: {},
                ShaderType.SHAKE: {},
                ShaderType.BLOOM: {},
                ShaderType.GRAYSCALE: {},
                ShaderType.CRT: {},
                ShaderType.RAYS: {}
            }

            # For the secret settings option in the settings menu, apply shaders for the selected option
            if (selected_shader := get_user_settings()['shader']) is not None:
                for shader_type in SHADER_MAP[selected_shader]:
                    self.set_effect(shader_type)
        else:
            # If shaders disabled, use temporary image as background
            from data.utils.assets import GRAPHICS
            self._background_image = GRAPHICS['temp_background']

    def set_effect(self, effect, **kwargs):
        if is_opengl:
            self._shader_manager.apply_shader(effect, **kwargs)

    def set_apply_arguments(self, effect, **kwargs):
        if is_opengl:
            self.shader_arguments[effect] = kwargs

    def clear_apply_arguments(self, effect):
        if is_opengl:
            self.shader_arguments[effect] = {}

    def clear_effect(self, effect):
        if is_opengl:
            self._shader_manager.remove_shader(effect)
            self.clear_apply_arguments(effect)

    def clear_all_effects(self, clear_arguments=False):
        if is_opengl:
            self._shader_manager.clear_shaders()

            if clear_arguments:
                for shader_type in self.shader_arguments:
                    self.shader_arguments[shader_type] = {}

    def draw(self):
        if is_opengl:
            self._shader_manager.draw(self.screen, self.shader_arguments)
        else:
            self._native_screen.blit(self.screen, (0, 0))

        self.flip()

        if is_opengl:
            self.screen.fill((0, 0, 0, 0))
        else:
            self.screen.fill((0, 0, 0))
            draw_background(self.screen, self._background_image)

    def update(self):
        self.draw()

    def handle_resize(self):
        self.screen = pygame.Surface(self.size, pygame.SRCALPHA)
        if is_opengl:
            self._shader_manager.handle_resize(self.size)
        else:
            draw_background(self.screen, self._background_image)

window = WindowManager(size=SCREEN_SIZE, resizable=True, opengl=is_opengl, fullscreen_desktop=is_fullscreen)