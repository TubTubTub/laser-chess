from data.constants import ShaderType
from array import array
from pathlib import Path
import moderngl

shader_path = (Path(__file__).parent / './shaders/').resolve()

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

class ShaderManager:
    def __init__(self, ctx: moderngl.Context, screen_size):
        self._ctx = ctx

        # self._ctx.enable(self._ctx.BLEND) # BLEND NEEDED FOR LIGHTMAP BUT BREAKS WITH SHADOWMAP
        # self._ctx.blend_func = ctx.SRC_ALPHA, ctx.ONE_MINUS_SRC_ALPHA

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

    def load_shader(self, shader_type):
        self._shader_passes[shader_type] = shader_pass_lookup[shader_type](self)

        vert_path = Path(shader_path / 'base.vert').resolve()
        frag_path = Path(shader_path / (shader_type + '.frag')).resolve()

        self._vert_shaders[shader_type] = vert_path.read_text()
        self._frag_shaders[shader_type] = frag_path.read_text()

        self.create_vao(shader_type)
    
    def create_vao(self, shader_type):
        program = self._ctx.program(vertex_shader=self._vert_shaders[shader_type], fragment_shader=self._frag_shaders[shader_type])
        self._programs[shader_type] = program

        self._vaos[shader_type] = self._ctx.vertex_array(self._programs[shader_type], [(self._opengl_buffer, '2f 2f', 'vert', 'texCoords')])

    def create_texture(self, shader_type):
        texture = self._ctx.texture(size=self._screen_size, components=4)
        texture.filter = (moderngl.NEAREST, moderngl.NEAREST)

        self._textures[shader_type] = texture
    
    def create_framebuffer(self, shader_type):
        self.create_texture(shader_type)
        self.framebuffers[shader_type] = self._ctx.framebuffer(color_attachments=[self._textures[shader_type]])
    
    def render_to_fbo(self, shader_type, texture, output_fbo=None, **kwargs):
        fbo = output_fbo or self.framebuffers[shader_type]
        fbo.use()
        texture.use(0)

        self._programs[shader_type]['image'] = 0
        for uniform, value in kwargs.items():
            self._programs[shader_type][uniform] = value
            
        self._vaos[shader_type].render(mode=moderngl.TRIANGLE_STRIP)
    
    def apply_shader(self, shader_type):
        if shader_type in self._shader_stack:
            raise ValueError('(ShaderManager) Shader already being applied!', shader_type)
        
        self.load_shader(shader_type)
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
    
    def calibrate_pygame_texture(self, pygame_texture):
        pygame_texture.use()
        self.framebuffers[ShaderType.BASE].use()
        self._calibration_vao.render(mode=moderngl.TRIANGLE_STRIP)
        pygame_texture.release()

        return self.get_fbo_texture(ShaderType.BASE)

    def draw(self, screen_texture):
        self._ctx.viewport = (0, 0, *self._screen_size)
        texture = self.calibrate_pygame_texture(screen_texture)

        for shader_type in self._shader_stack:
            self._shader_passes[shader_type].apply(texture)
            texture = self.get_fbo_texture(shader_type)
        # print(texture.read())
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

class LightMap:
    def __init__(self, shader_manager: ShaderManager):
        self._shader_manager = shader_manager
        self._light_size = 600

        from data.assets import GRAPHICS
        self._test_surface = GRAPHICS['final_8'].get_view('1')

        shader_manager.load_shader(ShaderType.SHADOWMAP)

        shader_manager.create_framebuffer(ShaderType.LIGHTMAP)

    def apply(self, texture):
        self._shader_manager._ctx.enable(self._shader_manager._ctx.BLEND)

        ShadowMap(self._shader_manager).apply(texture)

        # self._shader_manager.get_fbo_texture(ShaderType.SHADOWMAP).write(self._test_surface)
        # self._shader_manager.get_fbo_texture(ShaderType.SHADOWMAP).swizzle = 'BRGA'


        shadow_map = self._shader_manager.get_fbo_texture(ShaderType.SHADOWMAP)
        shadow_map.use(1)

        self._shader_manager.render_to_fbo(ShaderType.LIGHTMAP, texture, shadowMap=1, resolution=(self._light_size, self._light_size))
        # self._shader_manager.render_to_fbo(ShaderType.LIGHTMAP, occlusion_texture, shadowMap=1)
        # self._shader_manager.render_to_fbo(ShaderType.LIGHTMAP, shadow_map)

        self._shader_manager._ctx.disable(self._shader_manager._ctx.BLEND)

class ShadowMap:
    def __init__(self, shader_manager: ShaderManager):
        self._shader_manager = shader_manager
        self._light_size = 600

        shader_manager.load_shader(ShaderType.OCCLUSION)
        
        texture = self._shader_manager._ctx.texture(size=(self._light_size, 1), components=4)
        texture.filter = (moderngl.LINEAR, moderngl.LINEAR) # TESTING CHANGE TO LINEAR
        texture.repeat_x = True
        texture.repeat_y = True

        self._shader_manager._textures[ShaderType.SHADOWMAP] = texture
        self._shader_manager.framebuffers[ShaderType.SHADOWMAP] = self._shader_manager._ctx.framebuffer(color_attachments=[texture])

    def apply(self, texture):
        Occlusion(self._shader_manager).apply(texture)
        occlusion_texture = self._shader_manager.get_fbo_texture(ShaderType.OCCLUSION)

        # self._shader_manager.render_to_fbo(ShaderType.SHADOWMAP, occlusion_texture, resolution=(self._light_size, self._light_size))
        self._shader_manager.render_to_fbo(ShaderType.SHADOWMAP, occlusion_texture)

class Occlusion:
    def __init__(self, shader_manager: ShaderManager):
        self._shader_manager = shader_manager
        self._shader_manager.create_framebuffer(ShaderType.OCCLUSION)

    def apply(self, texture):
        self._shader_manager.render_to_fbo(ShaderType.OCCLUSION, texture)

shader_pass_lookup = {
    ShaderType.CALIBRATE: lambda *args: None,
    ShaderType.BASE: Base,
    ShaderType.BLOOM: Bloom,
    ShaderType.BLUR: Blur,
    ShaderType.HIGHLIGHT: Highlight,
    ShaderType.GRAYSCALE: Grayscale,
    ShaderType.CRT: CRT,
    ShaderType.SHADOWMAP: ShadowMap,
    ShaderType.OCCLUSION: Occlusion,
    ShaderType.LIGHTMAP: LightMap,
}