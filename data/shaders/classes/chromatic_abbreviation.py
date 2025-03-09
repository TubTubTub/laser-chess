import pygame
from data.utils.constants import ShaderType
from data.shaders.protocol import SMProtocol

CHROMATIC_ABBREVIATION_INTENSITY = 2.0

class ChromaticAbbreviation:
    def __init__(self, shader_manager: SMProtocol):
        self._shader_manager = shader_manager

        self._shader_manager.create_framebuffer(ShaderType.CHROMATIC_ABBREVIATION)

    def apply(self, texture):
        mouse_pos = (pygame.mouse.get_pos()[0] / texture.size[0], pygame.mouse.get_pos()[1] / texture.size[1])
        self._shader_manager.render_to_fbo(ShaderType.CHROMATIC_ABBREVIATION, texture, mouseFocusPoint=mouse_pos, enabled=pygame.mouse.get_pressed()[0], intensity=CHROMATIC_ABBREVIATION_INTENSITY)