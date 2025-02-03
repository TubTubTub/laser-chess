from data.constants import ShaderType
from data.shaders.protocol import SMProtocol

class _Occlusion:
    def __init__(self, shader_manager: SMProtocol):
        self._shader_manager = shader_manager

    def apply(self, texture, occlusion_colour=(255, 0, 0)):
        self._shader_manager.create_framebuffer(ShaderType._OCCLUSION, size=texture.size)
        self._shader_manager.render_to_fbo(ShaderType._OCCLUSION, texture, checkColour=occlusion_colour)