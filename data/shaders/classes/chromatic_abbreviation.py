import pygame
from data.constants import ShaderType
from data.shaders.protocol import SMProtocol

class ChromaticAbbreviation:
    def __init__(self, shader_manager: SMProtocol):
        self._shader_manager = shader_manager

        self._shader_manager.create_framebuffer(ShaderType.CHROMATIC_ABBREVIATION)

    def apply(self, texture):
        self._shader_manager.render_to_fbo(ShaderType.CHROMATIC_ABBREVIATION, texture, time=pygame.time.get_ticks() / 1000)