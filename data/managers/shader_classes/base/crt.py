from data.constants import ShaderType
from data.managers.shader import ShaderManager

class CRT:
    def __init__(self, shader_manager: ShaderManager):
        self._shader_manager = shader_manager

        shader_manager.create_framebuffer(ShaderType.CRT)
    
    def apply(self, texture):
        self._shader_manager.render_to_fbo(ShaderType.CRT, texture)