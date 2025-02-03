import moderngl
from data.constants import ShaderType
from data.managers.shader import ShaderManager

class _Blend:
    def __init__(self, shader_manager: ShaderManager):
        self._shader_manager = shader_manager

        self._shader_manager.create_framebuffer(ShaderType._BLEND)

    def apply(self, texture, texture_2, texture_2_pos):
        self._shader_manager._ctx.blend_func = (moderngl.SRC_ALPHA, moderngl.ONE)

        relative_size = (texture_2.size[0] / texture.size[0], texture_2.size[1] / texture.size[1])
        opengl_pos = (texture_2_pos[0], 1 - texture_2_pos[1] - relative_size[1])

        texture_2.use(1)
        self._shader_manager.render_to_fbo(ShaderType._BLEND, texture, image2=1, image2Pos=opengl_pos, relativeSize=relative_size)
        self._shader_manager._ctx.blend_func = moderngl.DEFAULT_BLENDING