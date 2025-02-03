from data.constants import ShaderType
from data.managers.shader import ShaderManager

class _Crop:
    def __init__(self, shader_manager: ShaderManager):
        self._shader_manager = shader_manager

    def apply(self, texture, relative_pos, relative_size):
        opengl_pos = (relative_pos[0], 1 - relative_pos[1] - relative_size[1])
        pixel_size = (int(relative_size[0] * texture.size[0]), int(relative_size[1] * texture.size[1]))

        self._shader_manager.create_framebuffer(ShaderType._CROP, size=pixel_size)

        self._shader_manager.render_to_fbo(ShaderType._CROP, texture, relativePos=opengl_pos, relativeSize=relative_size)