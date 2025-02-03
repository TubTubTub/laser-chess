from data.constants import ShaderType
from data.shaders.protocol import SMProtocol
from data.shaders.classes.blur import _Blur
from data.shaders.classes.highlight_colour import _HighlightColour
from data.shaders.classes.highlight_brightness import _HighlightBrightness


BLOOM_INTENSITY = 0.6

class Bloom:
    def __init__(self, shader_manager: SMProtocol):
        self._shader_manager = shader_manager
        
        shader_manager.load_shader(ShaderType._BLUR)
        shader_manager.load_shader(ShaderType._HIGHLIGHT_BRIGHTNESS)
        shader_manager.load_shader(ShaderType._HIGHLIGHT_COLOUR)
        shader_manager.load_shader(ShaderType._OCCLUSION)

        shader_manager.create_framebuffer(ShaderType.BLOOM)
        shader_manager.create_framebuffer(ShaderType._BLUR)
        shader_manager.create_framebuffer(ShaderType._HIGHLIGHT_BRIGHTNESS)
        shader_manager.create_framebuffer(ShaderType._HIGHLIGHT_COLOUR)
        shader_manager.create_framebuffer(ShaderType._OCCLUSION)
    
    def apply(self, texture, occlusion_surface=None, occlusion_colours=[], occlusion_intensity=BLOOM_INTENSITY, brightness_intensity=BLOOM_INTENSITY, colour_intensity=BLOOM_INTENSITY):
        if occlusion_surface:
            occlusion_glare_texture = self._shader_manager.calibrate_pygame_surface(occlusion_surface)
            _Blur(self._shader_manager).apply(occlusion_glare_texture)
            
            self._shader_manager.get_fbo_texture(ShaderType._BLUR).use(1)
            self._shader_manager.render_to_fbo(ShaderType.BLOOM, texture, blurredImage=1, intensity=occlusion_intensity)

            texture = self._shader_manager.get_fbo_texture(ShaderType.BLOOM)
            
        _HighlightBrightness(self._shader_manager).apply(texture, intensity=brightness_intensity)
        highlight_texture = self._shader_manager.get_fbo_texture(ShaderType._HIGHLIGHT_BRIGHTNESS)

        for colour in occlusion_colours:
            _HighlightColour(self._shader_manager).apply(texture, old_highlight=highlight_texture, colour=colour, intensity=colour_intensity)
            highlight_texture = self._shader_manager.get_fbo_texture(ShaderType._HIGHLIGHT_COLOUR)

        _Blur(self._shader_manager).apply(highlight_texture)
        
        self._shader_manager.get_fbo_texture(ShaderType._BLUR).use(1)
        self._shader_manager.render_to_fbo(ShaderType.BLOOM, texture, blurredImage=1, intensity=BLOOM_INTENSITY)