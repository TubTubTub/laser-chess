import pygame
from data.constants import ShaderType
from data.managers.shader import ShaderManager
from data.managers.shader_classes.shadowmap import _Shadowmap

LIGHT_RESOLUTION = 256

class _Lightmap:
    def __init__(self, shader_manager: ShaderManager):
        self._shader_manager = shader_manager

        shader_manager.load_shader(ShaderType._SHADOWMAP)

    def apply(self, texture, colour, occlusion=None, falloff=0.0, clamp=(-180, 180)):
        self._shader_manager.create_framebuffer(ShaderType._LIGHTMAP, size=texture.size)
        self._shader_manager._ctx.enable(self._shader_manager._ctx.BLEND)

        _ShadowMap(self._shader_manager).apply(texture, occlusion)
        shadow_map = self._shader_manager.get_fbo_texture(ShaderType._SHADOWMAP)

        self._shader_manager.render_to_fbo(ShaderType._LIGHTMAP, shadow_map, resolution=LIGHT_RESOLUTION, lightColour=colour, falloff=falloff, angleClamp=clamp)

        self._shader_manager._ctx.disable(self._shader_manager._ctx.BLEND)