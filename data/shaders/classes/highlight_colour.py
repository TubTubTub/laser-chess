from data.constants import ShaderType
from data.shaders.protocol import SMProtocol

class _HighlightColour:
    def __init__(self, shader_manager: SMProtocol):
        self._shader_manager = shader_manager

        shader_manager.create_framebuffer(ShaderType._HIGHLIGHT_COLOUR)
    
    def apply(self, texture, old_highlight, colour, intensity):
        old_highlight.use(1)
        self._shader_manager.render_to_fbo(ShaderType._HIGHLIGHT_COLOUR, texture, highlight=1, colour=colour, threshold=0.1, intensity=intensity)