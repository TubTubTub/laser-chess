from data.constants import ShaderType
from array import array
from pathlib import Path
import moderngl
from random import randint

shader_path = (Path(__file__).parent / '../shaders/').resolve()

pygame_quad_array = array('f', [
    -1.0, 1.0, 0.0, 0.0,
    1.0, 1.0, 1.0, 0.0,
    -1.0, -1.0, 0.0, 1.0,
    1.0, -1.0, 1.0, 1.0,
])

opengl_quad_array = array('f', [
    -1.0, -1.0, 0.0, 0.0,
    1.0, -1.0, 1.0, 0.0,
    -1.0, 1.0, 0.0, 1.0,
    1.0, 1.0, 1.0, 1.0,
])

HIGHLIGHT_THRESHOLD = 0.7
HIGHLIGHT_INTENSITY = 0.3
BLUR_ITERATIONS = 10
LIGHT_RESOLUTION = 256

class ShaderManager:
    def __init__(self, ctx: moderngl.Context, screen_size):
        self._ctx = ctx
        self._ctx.gc_mode = 'auto'

        self._screen_size = screen_size
        self._opengl_buffer = self._ctx.buffer(data=opengl_quad_array)
        self._pygame_buffer = self._ctx.buffer(data=pygame_quad_array)
        self._shader_stack = [ShaderType.BASE]

        self._vert_shaders = {}
        self._frag_shaders = {}
        self._programs = {}
        self._vaos = {}
        self._textures = {}
        self.framebuffers = {}
        self._shader_passes = {}

        self.load_shader(ShaderType.BASE)
        self._calibration_vao = self._ctx.vertex_array(self._programs[ShaderType.BASE], [(self._pygame_buffer, '2f 2f', 'vert', 'texCoords')])

    def load_shader(self, shader_type, **kwargs):
        self._shader_passes[shader_type] = shader_pass_lookup[shader_type](self, **kwargs)

        vert_path = Path(shader_path / 'base.vert').resolve()
        frag_path = Path(shader_path / (shader_type.replace('_', '') + '.frag')).resolve()

        self._vert_shaders[shader_type] = vert_path.read_text()
        self._frag_shaders[shader_type] = frag_path.read_text()

        self.create_vao(shader_type)
    
    def clear_shaders(self):
        self._shader_stack = [ShaderType.BASE]
    
    def create_vao(self, shader_type):
        program = self._ctx.program(vertex_shader=self._vert_shaders[shader_type], fragment_shader=self._frag_shaders[shader_type])
        self._programs[shader_type] = program

        self._vaos[shader_type] = self._ctx.vertex_array(self._programs[shader_type], [(self._opengl_buffer, '2f 2f', 'vert', 'texCoords')])
    
    def create_framebuffer(self, shader_type, size=None, filter=moderngl.NEAREST):
        texture_size = size or self._screen_size
        texture = self._ctx.texture(size=texture_size, components=4)
        texture.filter = (filter, filter)

        self._textures[shader_type] = texture
        self.framebuffers[shader_type] = self._ctx.framebuffer(color_attachments=[self._textures[shader_type]])
    
    def render_to_fbo(self, shader_type, texture, output_fbo=None, **kwargs):
        fbo = output_fbo or self.framebuffers[shader_type]
        fbo.use()
        texture.use(0)

        self._programs[shader_type]['image'] = 0
        for uniform, value in kwargs.items():
            self._programs[shader_type][uniform] = value
            
        self._vaos[shader_type].render(mode=moderngl.TRIANGLE_STRIP)
    
    def apply_shader(self, shader_type, **kwargs):
        if shader_type in self._shader_stack:
            return
            raise ValueError('(ShaderManager) Shader already being applied!', shader_type)
        
        self.load_shader(shader_type, **kwargs)
        self._shader_stack.append(shader_type)
    
    def remove_shader(self, shader_type):
        self._shader_stack.remove(shader_type)
    
    def render_output(self):
        output_shader_type = self._shader_stack[-1]
        self._ctx.screen.use() # IMPORTANT

        self.get_fbo_texture(output_shader_type).use(0)
        self._programs[output_shader_type]['image'] = 0

        self._vaos[output_shader_type].render(mode=moderngl.TRIANGLE_STRIP) # SOMETHING ABOUT DRAWING FLIPS THE

    def get_fbo_texture(self, shader_type):
        return self.framebuffers[shader_type].color_attachments[0]
    
    def calibrate_pygame_surface(self, pygame_surface):
        texture = self._ctx.texture(pygame_surface.size, 4)
        texture.filter = (moderngl.NEAREST, moderngl.NEAREST)
        texture.swizzle = 'BGRA'
        texture.write(pygame_surface.get_view('1'))

        texture.use()
        self.framebuffers[ShaderType.BASE].use()
        self._calibration_vao.render(mode=moderngl.TRIANGLE_STRIP)
        texture.release()

        return self.get_fbo_texture(ShaderType.BASE)

    def draw(self, surface):
        self._ctx.viewport = (0, 0, *self._screen_size)
        texture = self.calibrate_pygame_surface(surface)

        for shader_type in self._shader_stack:
            self._shader_passes[shader_type].apply(texture)
            texture = self.get_fbo_texture(shader_type)

        self.render_output()
    
    def __del__(self):
        self.cleanup()
    
    def cleanup(self):
        self._pygame_buffer.release()
        self._opengl_buffer.release()
        for program in self._programs:
            self._programs[program].release()
        for texture in self._textures:
            self._textures[texture].release()
        for vao in self._vaos:
            self._vaos[vao].release()
        for framebuffer in self.framebuffers:
            self.framebuffers[framebuffer].release()
    
    def handle_resize(self, new_screen_size):
        self._screen_size = new_screen_size

        for shader_type in self.framebuffers:
            filter = self._textures[shader_type].filter[0]
            self.create_framebuffer(shader_type, size=self._screen_size, filter=filter) # RECREATE FRAMEBUFFER TO PREVENT SCALING ISSUES

class Base:
    def __init__(self, shader_manager: ShaderManager):
        self._shader_manager = shader_manager

        self._shader_manager.create_framebuffer(ShaderType.BASE)
    
    def apply(self, texture):
        self._shader_manager.render_to_fbo(ShaderType.BASE, texture)

class Grayscale:
    def __init__(self, shader_manager: ShaderManager):
        self._shader_manager = shader_manager

        shader_manager.create_framebuffer(ShaderType.GRAYSCALE)
    
    def apply(self, texture):
        self._shader_manager.render_to_fbo(ShaderType.GRAYSCALE, texture)

class CRT:
    def __init__(self, shader_manager: ShaderManager):
        self._shader_manager = shader_manager

        shader_manager.create_framebuffer(ShaderType.CRT)
    
    def apply(self, texture):
        self._shader_manager.render_to_fbo(ShaderType.CRT, texture)

class Bloom:
    def __init__(self, shader_manager: ShaderManager):
        self._shader_manager = shader_manager
        
        shader_manager.load_shader(ShaderType.BLUR)
        shader_manager.load_shader(ShaderType.HIGHLIGHT)

        shader_manager.create_framebuffer(ShaderType.BLOOM)
        shader_manager.create_framebuffer(ShaderType.BLUR)
        shader_manager.create_framebuffer(ShaderType.HIGHLIGHT)
    
    def apply(self, texture):
        Highlight(self._shader_manager).apply(texture)
        Blur(self._shader_manager).apply(self._shader_manager.get_fbo_texture(ShaderType.HIGHLIGHT))
        
        self._shader_manager.get_fbo_texture(ShaderType.BLUR).use(1)
        self._shader_manager.render_to_fbo(ShaderType.BLOOM, texture, blurredImage=1)

class Highlight:
    def __init__(self, shader_manager: ShaderManager):
        self._shader_manager = shader_manager

        shader_manager.create_framebuffer(ShaderType.HIGHLIGHT)
    
    def apply(self, texture):
        self._shader_manager.render_to_fbo(ShaderType.HIGHLIGHT, texture, threshold=HIGHLIGHT_THRESHOLD, intensity=HIGHLIGHT_INTENSITY)

class Blur:
    def __init__(self, shader_manager: ShaderManager):
        self._shader_manager = shader_manager

        shader_manager.create_framebuffer(ShaderType.BLUR)

        shader_manager.create_framebuffer("blurPing")
        shader_manager.create_framebuffer("blurPong")
    
    def apply(self, texture):
        self._shader_manager.get_fbo_texture("blurPong").write(texture.read())

        for _ in range(BLUR_ITERATIONS):
            self._shader_manager.render_to_fbo(
                ShaderType.BLUR,
                texture=self._shader_manager.get_fbo_texture("blurPong"),
                output_fbo=self._shader_manager.framebuffers["blurPing"],
                passes=5,
                horizontal=True
            )
            self._shader_manager.render_to_fbo(
                ShaderType.BLUR,
                texture=self._shader_manager.get_fbo_texture("blurPing"),
                output_fbo=self._shader_manager.framebuffers["blurPong"],
                passes=5,
                horizontal=False
            )

        self._shader_manager.render_to_fbo(ShaderType.BLUR, self._shader_manager.get_fbo_texture("blurPong"))

class Rays:
    def __init__(self, shader_manager: ShaderManager, lights): # pos relative to screen, radius pixels
        self._shader_manager = shader_manager
        self._lights = lights

        shader_manager.load_shader(ShaderType._LIGHTMAP)
        shader_manager.load_shader(ShaderType._BLEND)
        shader_manager.load_shader(ShaderType._CROP)
        shader_manager.create_framebuffer(ShaderType.RAYS)
    
    # def get_cropped_texture(self, texture, light_pos, light_radius): # if this approach to edges doesn't work, fill edge in with occluder instead
    #     screen_size = self._shader_manager._screen_size
    #     pos = (light_pos[0] * screen_size[0], light_pos[1] * screen_size[1])

    #     topleft = (max(0, pos[0] - light_radius), max(0, pos[1] - light_radius))
    #     bottomright = (min(texture.size[0], pos[0] + light_radius), min(texture.size[1], pos[1] + light_radius))

    #     new_surface = pygame.Surface((bottomright[0] - topleft[0], bottomright[1] - topleft[1]))
    #     new_surface.blit(texture, (-pos[0], -pos[1]))
    #     return new_surface
    
    def apply(self, texture):
        final_texture = texture

        for light_pos, light_radius, light_colour in self._lights:
            light_topleft = (light_pos[0] - (light_radius * texture.size[1] / texture.size[0]), light_pos[1] - light_radius)
            relative_size = (light_radius * 2 * texture.size[1] / texture.size[0], light_radius * 2)

            _Crop(self._shader_manager).apply(texture, relative_pos=light_topleft, relative_size=relative_size)
            cropped_texture = self._shader_manager.get_fbo_texture(ShaderType._CROP)

            _LightMap(self._shader_manager).apply(cropped_texture, light_colour)
            light_map = self._shader_manager.get_fbo_texture(ShaderType._LIGHTMAP)
            
            _Blend(self._shader_manager).apply(final_texture, light_map, light_topleft)
            final_texture = self._shader_manager.get_fbo_texture(ShaderType._BLEND)
        
        self._shader_manager.render_to_fbo(ShaderType.RAYS, final_texture)

class _LightMap:
    def __init__(self, shader_manager: ShaderManager):
        self._shader_manager = shader_manager

        shader_manager.load_shader(ShaderType._SHADOWMAP)

    def apply(self, texture, light_colour):
        self._shader_manager.create_framebuffer(ShaderType._LIGHTMAP, size=texture.size)
        self._shader_manager._ctx.enable(self._shader_manager._ctx.BLEND)

        _ShadowMap(self._shader_manager).apply(texture)

        # shadow_map = self._shader_manager.get_fbo_texture(ShaderType._SHADOWMAP)
        # shadow_map.use(1)
        # occlusionMap = self._shader_manager.get_fbo_texture(ShaderType._OCCLUSION)
        # occlusionMap.use(2)

        self._shader_manager.render_to_fbo(ShaderType._LIGHTMAP, self._shader_manager.get_fbo_texture(ShaderType._SHADOWMAP), resolution=LIGHT_RESOLUTION, lightColour=light_colour)

        self._shader_manager._ctx.disable(self._shader_manager._ctx.BLEND)

class _ShadowMap:
    def __init__(self, shader_manager: ShaderManager):
        self._shader_manager = shader_manager

        shader_manager.load_shader(ShaderType._OCCLUSION)

    def apply(self, texture):
        self._shader_manager.create_framebuffer(ShaderType._SHADOWMAP, size=(texture.size[0], 1), filter=moderngl.LINEAR)

        _Occlusion(self._shader_manager).apply(texture)
        occlusion_texture = self._shader_manager.get_fbo_texture(ShaderType._OCCLUSION)

        self._shader_manager.render_to_fbo(ShaderType._SHADOWMAP, occlusion_texture, resolution=LIGHT_RESOLUTION)

class _Occlusion:
    def __init__(self, shader_manager: ShaderManager):
        self._shader_manager = shader_manager

    def apply(self, texture):
        self._shader_manager.create_framebuffer(ShaderType._OCCLUSION, size=texture.size)
        self._shader_manager.render_to_fbo(ShaderType._OCCLUSION, texture)

class _Blend:
    def __init__(self, shader_manager: ShaderManager):
        self._shader_manager = shader_manager

        self._shader_manager.create_framebuffer(ShaderType._BLEND)

    def apply(self, texture, texture_2, texture_2_pos):
        # from data.assets import GRAPHICS
        # self._test_surface = GRAPHICS['overlay'].get_view('1')
        # self._shader_manager.create_framebuffer(ShaderType._OCCLUSION, size=(200, 200))
        # self._shader_manager.get_fbo_texture(ShaderType._OCCLUSION).write(self._test_surface)
        # self._shader_manager.get_fbo_texture(ShaderType._OCCLUSION).use(1)
        # texture_2 = self._shader_manager.get_fbo_texture(ShaderType._OCCLUSION)

        self._shader_manager._ctx.blend_func = (moderngl.SRC_ALPHA, moderngl.ONE)

        relative_size = (texture_2.size[0] / texture.size[0], texture_2.size[1] / texture.size[1])
        opengl_pos = (texture_2_pos[0], 1 - texture_2_pos[1] - relative_size[1])

        texture_2.use(1)
        self._shader_manager.render_to_fbo(ShaderType._BLEND, texture, image2=1, image2Pos=opengl_pos, relativeSize=relative_size)
        self._shader_manager._ctx.blend_func = moderngl.DEFAULT_BLENDING

class _Crop:
    def __init__(self, shader_manager: ShaderManager):
        self._shader_manager = shader_manager

    def apply(self, texture, relative_pos, relative_size):
        opengl_pos = (relative_pos[0], 1 - relative_pos[1] - relative_size[1])
        pixel_size = (int(relative_size[0] * texture.size[0]), int(relative_size[1] * texture.size[1]))

        self._shader_manager.create_framebuffer(ShaderType._CROP, size=pixel_size)

        self._shader_manager.render_to_fbo(ShaderType._CROP, texture, relativePos=opengl_pos, relativeSize=relative_size)

shader_pass_lookup = {
    ShaderType.CALIBRATE: lambda *args: None,
    ShaderType.BASE: Base,
    ShaderType.BLOOM: Bloom,
    ShaderType.BLUR: Blur,
    ShaderType.HIGHLIGHT: Highlight,
    ShaderType.GRAYSCALE: Grayscale,
    ShaderType.CRT: CRT,
    ShaderType.RAYS: Rays,
    ShaderType._SHADOWMAP: _ShadowMap,
    ShaderType._OCCLUSION: _Occlusion,
    ShaderType._LIGHTMAP: _LightMap,
    ShaderType._BLEND: _Blend,
    ShaderType._CROP: _Crop,
}