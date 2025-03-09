from data.utils.constants import ShaderType
from data.shaders.protocol import SMProtocol
from random import randint

SHAKE_INTENSITY = 3

class Shake:
    def __init__(self, shader_manager: SMProtocol):
        self._shader_manager = shader_manager

        self._shader_manager.create_framebuffer(ShaderType.SHAKE)

    def apply(self, texture, intensity=SHAKE_INTENSITY):
        displacement = (randint(-intensity, intensity) / 1000, randint(-intensity, intensity) / 1000)
        self._shader_manager.render_to_fbo(ShaderType.SHAKE, texture, displacement=displacement)