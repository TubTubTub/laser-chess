from data.constants import ShaderType
from data.managers.shader import ShaderManager

HIGHLIGHT_THRESHOLD = 0.9

class _HighlightBrightness:
    def __init__(self, shader_manager: ShaderManager):
        self._shader_manager = shader_manager

        shader_manager.create_framebuffer(ShaderType._HIGHLIGHT_BRIGHTNESS)
    
    def apply(self, texture, intensity):
        self._shader_manager.render_to_fbo(ShaderType._HIGHLIGHT_BRIGHTNESS, texture, threshold=HIGHLIGHT_THRESHOLD, intensity=intensity)