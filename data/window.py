import pygame
from data.constants import ShaderType
from data.components.animation import animation
from random import randint
import moderngl
from array import array
from data.constants import SCREEN_SIZE
from pathlib import Path
from data.utils.data_helpers import get_user_settings

vertex_shader = (Path(__file__).parent / './shaders/base.vert').resolve().read_text()
fragment_shader = (Path(__file__).parent / './shaders/base.frag').resolve().read_text()

quad_array = array('f', [
    -1.0, 1.0, 0.0, 0.0,
    1.0, 1.0, 1.0, 0.0,
    -1.0, -1.0, 0.0, 1.0,
    1.0, -1.0, 1.0, 1.0,
])

class WindowManager(pygame.Window):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._screen_shake = None

        self._ctx = moderngl.create_context()
        quad_buffer = self._ctx.buffer(data=quad_array)
        self._program = self._ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        self._render_object = self._ctx.vertex_array(self._program, [(quad_buffer, '2f 2f', 'vert', 'texCoords')])
    
    def get_size(self):
        return self.size
    
    def to_texture(self):
        texture = self._ctx.texture(self.size, 4)
        texture.filter = (moderngl.NEAREST, moderngl.NEAREST)
        texture.swizzle = 'BGRA'
        texture.write(self.get_surface().get_view('1'))

        return texture
    
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
    
    def render_1(self):
        frame_texture = self.to_texture()
        frame_texture.use(0)

        self._program['screenTexture'] = 0
        self._render_object.render(mode=moderngl.TRIANGLE_STRIP)

        frame_texture.release()
    
    def render_2(self):
        contrast_texture = self._ctx.texture(size=self.size, components=4)
        blur_texture = self._ctx.texture(size=self.size, components=4)
        bloom_texture = self._ctx.texture(size=self.size, components=4)

        contrast_fbo = self._ctx.framebuffer(color_attachments=contrast_texture)
        blur_fbo = self._ctx.framebuffer(color_attachments=blur_texture)
        bloom_fbo = self._ctx.framebuffer(color_attachments=bloom_texture)

        screen_texture = self.to_texture()
        screen_texture.use(0)

        contrast_fbo.use()
        self._render_object
        
    
    def draw(self):
        self._ctx.viewport = (0, 0, *self.size)
        self.render_1()
        self.flip()
    
    def update(self):
        if self._screen_shake is not None:
            surface = self.get_surface()
            surface_copy = surface.copy()

            surface.fill((0, 0, 0))
            surface.blit(surface_copy, (randint(0, self._screen_shake) - self._screen_shake / 2, randint(0, self._screen_shake) - self._screen_shake / 2))

        self.draw()

is_fullscreen = get_user_settings()['displayMode'] == 'fullscreen'
window = WindowManager(size=SCREEN_SIZE, opengl=True, fullscreen=is_fullscreen, resizable=True)
screen = window.get_surface()