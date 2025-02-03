import moderngl
from data.constants import ShaderType
from data.managers.shader import ShaderManager
from data.managers.shader_classes.occlusion import _Occlusion

LIGHT_RESOLUTION = 256

class _Shadowmap:
    def __init__(self, shader_manager: ShaderManager):
        self._shader_manager = shader_manager

        shader_manager.load_shader(ShaderType._OCCLUSION)

    def apply(self, texture, occlusion_texture=None):
        self._shader_manager.create_framebuffer(ShaderType._SHADOWMAP, size=(texture.size[0], 1), filter=moderngl.LINEAR)

        if occlusion_texture is None:
            _Occlusion(self._shader_manager).apply(texture)
            occlusion_texture = self._shader_manager.get_fbo_texture(ShaderType._OCCLUSION)

        self._shader_manager.render_to_fbo(ShaderType._SHADOWMAP, occlusion_texture, resolution=LIGHT_RESOLUTION)