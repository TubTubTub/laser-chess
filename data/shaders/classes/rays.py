from data.constants import ShaderType
from data.shaders.protocol import SMProtocol
from data.shaders.classes.crop import _Crop
from data.shaders.classes.lightmap import _Lightmap
from data.shaders.classes.blend import _Blend

class Rays:
    def __init__(self, shader_manager: SMProtocol, lights): # pos relative to screen, radius pixels
        self._shader_manager = shader_manager
        self._lights = lights

        shader_manager.load_shader(ShaderType._LIGHTMAP)
        shader_manager.load_shader(ShaderType._BLEND)
        shader_manager.load_shader(ShaderType._CROP)
        shader_manager.create_framebuffer(ShaderType.RAYS)
    
    def apply(self, texture, occlusion=None):
        final_texture = texture

        for pos, radius, colour, *args in self._lights:
            light_topleft = (pos[0] - (radius * texture.size[1] / texture.size[0]), pos[1] - radius)
            relative_size = (radius * 2 * texture.size[1] / texture.size[0], radius * 2)

            _Crop(self._shader_manager).apply(texture, relative_pos=light_topleft, relative_size=relative_size)
            cropped_texture = self._shader_manager.get_fbo_texture(ShaderType._CROP)

            if occlusion:
                occlusion_texture = self._shader_manager.calibrate_pygame_surface(occlusion)
                _Crop(self._shader_manager).apply(occlusion_texture, relative_pos=light_topleft, relative_size=relative_size)
                occlusion_texture = self._shader_manager.get_fbo_texture(ShaderType._CROP)
            else:
                occlusion_texture = None

            _Lightmap(self._shader_manager).apply(cropped_texture, colour, occlusion_texture, *args)
            light_map = self._shader_manager.get_fbo_texture(ShaderType._LIGHTMAP)
            
            _Blend(self._shader_manager).apply(final_texture, light_map, light_topleft)
            final_texture = self._shader_manager.get_fbo_texture(ShaderType._BLEND)
        
        self._shader_manager.render_to_fbo(ShaderType.RAYS, final_texture)