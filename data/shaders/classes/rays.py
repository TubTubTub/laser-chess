from data.shaders.classes.lightmap import _Lightmap
from data.shaders.classes.blend import _Blend
from data.shaders.protocol import SMProtocol
from data.shaders.classes.crop import _Crop
from data.utils.constants import ShaderType

class Rays:
    def __init__(self, shader_manager: SMProtocol, lights):
        self._shader_manager = shader_manager
        self._lights = lights

        # Load all necessary shaders
        shader_manager.load_shader(ShaderType._LIGHTMAP)
        shader_manager.load_shader(ShaderType._BLEND)
        shader_manager.load_shader(ShaderType._CROP)
        shader_manager.create_framebuffer(ShaderType.RAYS)

    def apply(self, texture, occlusion=None, softShadow=0.3):
        """
        Applies the light rays effect to a given texture.

        Args:
            texture (moderngl.Texture): The texture to apply the effect to.
            occlusion (pygame.Surface, optional): A Pygame mask surface to use as the occlusion texture. Defaults to None.
        """
        final_texture = texture

        # Iterate through array containing light information
        for pos, radius, colour, *args in self._lights:
            # Topleft of light source square
            light_topleft = (pos[0] - (radius * texture.size[1] / texture.size[0]), pos[1] - radius)
            # Relative size of light compared to texture
            relative_size = (radius * 2 * texture.size[1] / texture.size[0], radius * 2)

            # Crop texture to light source diameter, and to position light source at the center
            _Crop(self._shader_manager).apply(texture, relative_pos=light_topleft, relative_size=relative_size)
            cropped_texture = self._shader_manager.get_fbo_texture(ShaderType._CROP)

            if occlusion:
                # Calibrate Pygame mask surface and crop it
                occlusion_texture = self._shader_manager.calibrate_pygame_surface(occlusion)
                _Crop(self._shader_manager).apply(occlusion_texture, relative_pos=light_topleft, relative_size=relative_size)
                occlusion_texture = self._shader_manager.get_fbo_texture(ShaderType._CROP)
            else:
                occlusion_texture = None

            # Apply lightmap shader, shadowmap and occlusion are included within the _Lightmap class
            _Lightmap(self._shader_manager).apply(cropped_texture, colour, softShadow, occlusion_texture, *args)
            light_map = self._shader_manager.get_fbo_texture(ShaderType._LIGHTMAP)

            # Blend the final result with the original texture
            _Blend(self._shader_manager).apply(final_texture, light_map, light_topleft)
            final_texture = self._shader_manager.get_fbo_texture(ShaderType._BLEND)

        self._shader_manager.render_to_fbo(ShaderType.RAYS, final_texture)