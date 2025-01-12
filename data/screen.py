import pygame
from data.constants import ScreenEffect
from data.components.animation import animation
from random import randint
import moderngl
from array import array
from pathlib import Path

vertex_shader = (Path(__file__).parent / './shaders/base.vert').resolve().read_text()
fragment_shader = (Path(__file__).parent / './shaders/crt.frag').resolve().read_text()

quad_array = array('f', [
    -1.0, 1.0, 0.0, 0.0,
    1.0, 1.0, 1.0, 0.0,
    -1.0, -1.0, 0.0, 1.0,
    1.0, -1.0, 1.0, 1.0,
])

class ScreenManager(pygame.Surface):
    def __init__(self):
        self._pygame_screen = pygame.display.get_surface()
        self._position = (0, 0)

        self._screen_shake = None

        self._ctx = moderngl.create_context()
        quad_buffer = self._ctx.buffer(data=quad_array)
        self._program = self._ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        self._render_object = self._ctx.vertex_array(self._program, [(quad_buffer, '2f 2f', 'vert', 'texCoords')])

        super().__init__(self._pygame_screen.size)
    
    def surface_to_texture(self, surface):
        texture = self._ctx.texture(surface.get_size(), 4)
        texture.filter = (moderngl.NEAREST, moderngl.NEAREST)
        texture.swizzle = 'BGRA'
        texture.write(surface.get_view('1'))
        return texture
    
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
    
    def draw(self):
        frame_texture = self.surface_to_texture(self)
        frame_texture.use(0)
        self._program['screenTexture'] = 0
        self._render_object.render(mode=moderngl.TRIANGLE_STRIP)
        
        pygame.display.flip()

        frame_texture.release()
    
    def update(self):
        if self._screen_shake is not None:
            self._position = (randint(0, self._screen_shake) - self._screen_shake / 2, randint(0, self._screen_shake) - self._screen_shake / 2)

        self.draw()

screen = ScreenManager()