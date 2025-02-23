from data.shaders.classes.highlight_brightness import _HighlightBrightness
from data.shaders.classes.highlight_colour import _HighlightColour
from data.shaders.protocol import SMProtocol
from data.shaders.classes.blur import _Blur
from data.constants import ShaderType

BLOOM_INTENSITY = 0.6

class Bloom:
    def __init__(self, shader_manager: SMProtocol):
        self._shader_manager = shader_manager
        
        shader_manager.load_shader(ShaderType._BLUR)
        shader_manager.load_shader(ShaderType._HIGHLIGHT_BRIGHTNESS)
        shader_manager.load_shader(ShaderType._HIGHLIGHT_COLOUR)

        shader_manager.create_framebuffer(ShaderType.BLOOM)
        shader_manager.create_framebuffer(ShaderType._BLUR)
        shader_manager.create_framebuffer(ShaderType._HIGHLIGHT_BRIGHTNESS)
        shader_manager.create_framebuffer(ShaderType._HIGHLIGHT_COLOUR)
    
    def apply(self, texture, highlight_surface=None, highlight_colours=[], surface_intensity=BLOOM_INTENSITY, brightness_intensity=BLOOM_INTENSITY, colour_intensity=BLOOM_INTENSITY):
        """
        Applies a bloom effect to a given texture.

        Args:
            texture (moderngl.Texture): Texture to apply bloom to.
            highlight_surface (pygame.Surface, optional): Surface to use as the highlights. Defaults to None.
            highlight_colours (list[list[int, int, int], ...], optional): Colours to use as the highlights. Defaults to [].
            surface_intensity (_type_, optional): Intensity of bloom applied to the highlight surface. Defaults to BLOOM_INTENSITY.
            brightness_intensity (_type_, optional): Intensity of bloom applied to the highlight brightness. Defaults to BLOOM_INTENSITY.
            colour_intensity (_type_, optional): Intensity of bloom applied to the highlight colours. Defaults to BLOOM_INTENSITY.
        """
        if highlight_surface:
            # Calibrate Pygame surface and apply blur
            glare_texture = self._shader_manager.calibrate_pygame_surface(highlight_surface)
            _Blur(self._shader_manager).apply(glare_texture)
            
            self._shader_manager.get_fbo_texture(ShaderType._BLUR).use(1)
            self._shader_manager.render_to_fbo(ShaderType.BLOOM, texture, blurredImage=1, intensity=surface_intensity)

            # Set bloom-applied texture as the base texture
            texture = self._shader_manager.get_fbo_texture(ShaderType.BLOOM)
        
        # Extract bright colours (highlights) from the texture
        _HighlightBrightness(self._shader_manager).apply(texture, intensity=brightness_intensity)
        highlight_texture = self._shader_manager.get_fbo_texture(ShaderType._HIGHLIGHT_BRIGHTNESS)

        # Use colour as highlights
        for colour in highlight_colours:
            _HighlightColour(self._shader_manager).apply(texture, old_highlight=highlight_texture, colour=colour, intensity=colour_intensity)
            highlight_texture = self._shader_manager.get_fbo_texture(ShaderType._HIGHLIGHT_COLOUR)

        # Apply Gaussian blur to highlights
        _Blur(self._shader_manager).apply(highlight_texture)
        
        # Add the pixel values for the highlights onto the base texture
        self._shader_manager.get_fbo_texture(ShaderType._BLUR).use(1)
        self._shader_manager.render_to_fbo(ShaderType.BLOOM, texture, blurredImage=1, intensity=BLOOM_INTENSITY)