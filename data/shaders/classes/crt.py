from data.utils.constants import ShaderType
from data.shaders.protocol import SMProtocol

class CRT:
    def __init__(self, shader_manager: SMProtocol):
        self._shader_manager = shader_manager

        shader_manager.create_framebuffer(ShaderType.CRT)

    def apply(self, texture):
        self._shader_manager.render_to_fbo(ShaderType.CRT, texture)